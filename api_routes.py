"""
API Routes for new Cartify features:
- Multilingual Chatbot
- Product Recommendations
- Wishlist
- Multilingual Support
"""

from flask import Blueprint, request, jsonify, session
from models import (
    db, User, Product, Order, OrderItem, Wishlist, ProductRecommendation,
    UserLanguagePreference, MultilingualChatMessage, NotificationPreference
)
from auth import login_required, get_current_user
from chatbot_service import chatbot
from recommendation_service import recommendation_engine
import uuid
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')


# ==================== CHATBOT ROUTES ====================

@api_bp.route('/chat/send', methods=['POST'])
def send_chat_message():
    """Send message to chatbot and get response"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        language = data.get('language', 'en')
        user = get_current_user()
        user_id = user.id if user else None
        
        # Get or create session ID
        session_id = session.get('chat_session', str(uuid.uuid4()))
        session['chat_session'] = session_id
        
        if not user_message:
            return jsonify({'success': False, 'error': 'Message cannot be empty'}), 400
        
        # Validate language
        if language not in UserLanguagePreference.SUPPORTED_LANGUAGES:
            language = 'en'
        
        # Generate chatbot response
        bot_response, intent, confidence = chatbot.generate_response(
            user_message,
            language=language,
            user_id=user_id
        )
        
        # Log message
        chat_log = chatbot.log_chat_message(
            user_id=user_id,
            session_id=session_id,
            language=language,
            user_message=user_message,
            bot_response=bot_response,
            intent=intent,
            confidence=confidence
        )
        
        return jsonify({
            'success': True,
            'message': bot_response,
            'intent': intent,
            'confidence': confidence,
            'language': language,
            'session_id': session_id
        }), 200
    
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/chat/history', methods=['GET'])
def get_chat_history():
    """Get chat history for current user"""
    try:
        user_id = get_current_user()
        session_id = session.get('chat_session')
        
        if not session_id:
            return jsonify({'success': True, 'messages': []}), 200
        
        messages = MultilingualChatMessage.query.filter_by(
            session_id=session_id
        ).order_by(MultilingualChatMessage.created_at).all()
        
        return jsonify({
            'success': True,
            'messages': [msg.to_dict() for msg in messages]
        }), 200
    
    except Exception as e:
        print(f"Chat history error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/chat/logs', methods=['GET'])
def get_chat_logs():
    """Get multilingual chat logs for current session"""
    try:
        session_id = request.args.get('session_id') or session.get('chat_session')
        if not session_id:
            return jsonify({'success': True, 'messages': []}), 200

        messages = MultilingualChatMessage.query.filter_by(
            session_id=session_id
        ).order_by(MultilingualChatMessage.created_at.asc()).limit(100).all()

        return jsonify({
            'success': True,
            'messages': [msg.to_dict() for msg in messages],
            'session_id': session_id
        }), 200
    except Exception as e:
        print(f"Chat logs error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/chat/session-clear', methods=['POST'])
def clear_chat_session():
    """Clear multilingual chat logs for a session"""
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id') or session.get('chat_session')

        if session_id:
            MultilingualChatMessage.query.filter_by(session_id=session_id).delete()
            db.session.commit()

        return jsonify({'success': True, 'message': 'Chat history cleared'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Clear chat session error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== WISHLIST ROUTES ====================

@api_bp.route('/wishlist/add', methods=['POST'])
@login_required
def add_to_wishlist():
    """Add product to wishlist"""
    try:
        user_id = get_current_user()
        data = request.get_json()
        product_id = data.get('product_id')
        
        if not product_id:
            return jsonify({'success': False, 'error': 'Product ID required'}), 400
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        
        # Check if already in wishlist
        existing = Wishlist.query.filter_by(
            user_id=user_id,
            product_id=product_id
        ).first()
        
        if existing:
            return jsonify({'success': False, 'message': 'Already in wishlist'}), 200
        
        # Add to wishlist
        wishlist_item = Wishlist(user_id=user_id, product_id=product_id)
        db.session.add(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Added to wishlist',
            'item': wishlist_item.to_dict()
        }), 201
    
    except Exception as e:
        print(f"Add to wishlist error: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/wishlist/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_wishlist(product_id):
    """Remove product from wishlist"""
    try:
        user_id = get_current_user()
        
        wishlist_item = Wishlist.query.filter_by(
            user_id=user_id,
            product_id=product_id
        ).first()
        
        if not wishlist_item:
            return jsonify({'success': False, 'error': 'Item not in wishlist'}), 404
        
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Removed from wishlist'}), 200
    
    except Exception as e:
        print(f"Remove from wishlist error: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/wishlist', methods=['GET'])
@login_required
def get_wishlist():
    """Get user's wishlist"""
    try:
        user_id = get_current_user()
        
        wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'success': True,
            'items': [item.to_dict() for item in wishlist_items],
            'count': len(wishlist_items)
        }), 200
    
    except Exception as e:
        print(f"Get wishlist error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== RECOMMENDATION ROUTES ====================

@api_bp.route('/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    """Get personalized product recommendations"""
    try:
        user_id = get_current_user()
        limit = request.args.get('limit', 5, type=int)
        
        # Get recommendations
        recommendations = recommendation_engine.get_user_recommendations(user_id, limit)
        
        # Save to database
        recommendation_engine.save_recommendations(user_id, recommendations)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'count': len(recommendations)
        }), 200
    
    except Exception as e:
        print(f"Recommendations error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/recommendations/<int:product_id>/feedback', methods=['POST'])
@login_required
def feedback_recommendation(product_id):
    """Submit feedback on a recommendation"""
    try:
        user_id = get_current_user()
        data = request.get_json()
        helpful = data.get('helpful', False)
        
        # Update recommendation feedback
        rec = ProductRecommendation.query.filter_by(
            user_id=user_id,
            product_id=product_id
        ).first()
        
        if rec:
            # Adjust score based on feedback
            if helpful:
                rec.score = min(rec.score + 0.1, 1.0)
            else:
                rec.score = max(rec.score - 0.1, 0.0)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Feedback recorded'
        }), 200
    
    except Exception as e:
        print(f"Recommendation feedback error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== LANGUAGE PREFERENCE ROUTES ====================

@api_bp.route('/language/preference', methods=['GET', 'POST'])
@login_required
def language_preference():
    """Get or set user's language preference"""
    try:
        user_id = get_current_user()
        
        if request.method == 'GET':
            pref = UserLanguagePreference.query.filter_by(user_id=user_id).first()
            if not pref:
                pref = UserLanguagePreference(user_id=user_id, language_code='en')
                db.session.add(pref)
                db.session.commit()
            
            return jsonify({
                'success': True,
                'preference': pref.to_dict()
            }), 200
        
        else:  # POST
            data = request.get_json()
            language_code = data.get('language_code', 'en')
            timezone = data.get('timezone', 'UTC')
            
            # Validate language
            if language_code not in UserLanguagePreference.SUPPORTED_LANGUAGES:
                return jsonify({'success': False, 'error': 'Unsupported language'}), 400
            
            pref = UserLanguagePreference.query.filter_by(user_id=user_id).first()
            if not pref:
                pref = UserLanguagePreference(user_id=user_id)
            
            pref.language_code = language_code
            pref.preferred_language_name = UserLanguagePreference.SUPPORTED_LANGUAGES[language_code]['name']
            pref.timezone = timezone
            pref.updated_at = datetime.utcnow()
            
            db.session.add(pref)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Language preference updated',
                'preference': pref.to_dict()
            }), 200
    
    except Exception as e:
        print(f"Language preference error: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/languages/supported', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages"""
    try:
        languages = []
        for code, info in UserLanguagePreference.SUPPORTED_LANGUAGES.items():
            languages.append({
                'code': code,
                'name': info['name'],
                'native_name': info['native']
            })
        
        return jsonify({
            'success': True,
            'languages': languages,
            'count': len(languages)
        }), 200
    
    except Exception as e:
        print(f"Supported languages error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== NOTIFICATION PREFERENCE ROUTES ====================

@api_bp.route('/notifications/preference', methods=['GET', 'POST'])
@login_required
def notification_preference():
    """Get or set user's notification preferences"""
    try:
        user_id = get_current_user()
        
        if request.method == 'GET':
            pref = NotificationPreference.query.filter_by(user_id=user_id).first()
            if not pref:
                pref = NotificationPreference(user_id=user_id)
                db.session.add(pref)
                db.session.commit()
            
            return jsonify({
                'success': True,
                'preference': pref.to_dict()
            }), 200
        
        else:  # POST
            data = request.get_json()
            
            pref = NotificationPreference.query.filter_by(user_id=user_id).first()
            if not pref:
                pref = NotificationPreference(user_id=user_id)
            
            pref.email_notifications = data.get('email_notifications', pref.email_notifications)
            pref.sms_notifications = data.get('sms_notifications', pref.sms_notifications)
            pref.push_notifications = data.get('push_notifications', pref.push_notifications)
            pref.notification_language = data.get('notification_language', pref.notification_language)
            pref.order_updates = data.get('order_updates', pref.order_updates)
            pref.promotional = data.get('promotional', pref.promotional)
            pref.weekly_recommendations = data.get('weekly_recommendations', pref.weekly_recommendations)
            pref.updated_at = datetime.utcnow()
            
            db.session.add(pref)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Notification preferences updated',
                'preference': pref.to_dict()
            }), 200
    
    except Exception as e:
        print(f"Notification preference error: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== SEARCH ROUTES ====================

@api_bp.route('/search', methods=['GET'])
def search_products():
    """Search for products (multilingual support)"""
    try:
        query = request.args.get('q', '').strip()
        language = request.args.get('lang', 'en')
        category = request.args.get('category', '')
        limit = request.args.get('limit', 10, type=int)
        
        if not query and not category:
            return jsonify({'success': False, 'error': 'Query or category required'}), 400
        
        # Build query
        q = Product.query.filter_by(is_active=True)
        
        if query:
            q = q.filter(
                (Product.name.ilike(f'%{query}%')) |
                (Product.description.ilike(f'%{query}%'))
            )
        
        if category:
            q = q.filter_by(category=category)
        
        products = q.order_by(Product.rating.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'products': [p.to_dict() for p in products],
            'count': len(products),
            'language': language
        }), 200
    
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== EXPORT ROUTES ====================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'success': True,
        'message': 'API is running',
        'version': '1.0',
        'timestamp': datetime.utcnow().isoformat()
    }), 200
