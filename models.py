from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    # Email verification fields
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(100), nullable=True)
    email_verification_expires = db.Column(db.DateTime, nullable=True)
    otp_secret = db.Column(db.String(32), nullable=True)
    otp_enabled = db.Column(db.Boolean, default=False)

    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True)
    cart_items = db.relationship('CartItem', backref='cart_user', lazy=True)
    reviews = db.relationship('Review', backref='reviewer', lazy=True)
    wishlist_items = db.relationship('Wishlist', backref='wishlist_user', lazy=True)
    recommendations = db.relationship('ProductRecommendation', backref='recommendation_user', lazy=True)
    chat_messages = db.relationship('MultilingualChatMessage', backref='chat_user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_email_verification_token(self):
        """Generate a secure token for email verification"""
        import secrets
        self.email_verification_token = secrets.token_urlsafe(32)
        self.email_verification_expires = datetime.utcnow() + timedelta(hours=24)
        return self.email_verification_token

    def verify_email_token(self, token):
        """Verify email verification token"""
        if (self.email_verification_token == token and
            self.email_verification_expires > datetime.utcnow()):
            self.email_verified = True
            self.email_verification_token = None
            self.email_verification_expires = None
            return True
        return False

    def generate_otp_secret(self):
        """Generate OTP secret for 2FA"""
        import pyotp
        self.otp_secret = pyotp.random_base32()
        return self.otp_secret

    def verify_otp(self, otp_code):
        """Verify OTP code"""
        if not self.otp_secret:
            return False
        import pyotp
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(otp_code)

    def get_otp_uri(self):
        """Get OTP URI for QR code generation"""
        import pyotp
        totp = pyotp.TOTP(self.otp_secret)
        return totp.provisioning_uri(name=self.email, issuer_name="Cartify")

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'is_admin': self.is_admin,
            'email_verified': self.email_verified,
            'otp_enabled': self.otp_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    stock_quantity = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    
    @property
    def in_stock(self):
        return self.stock_quantity > 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'image': self.image_url,
            'in_stock': self.in_stock,
            'rating': self.rating,
            'reviews': self.review_count,
            'source': 'Database'
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    shipping_city = db.Column(db.String(50), nullable=False)
    shipping_state = db.Column(db.String(50), nullable=False)
    shipping_pincode = db.Column(db.String(10), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), default='pending')
    order_status = db.Column(db.String(20), default='pending')
    shipping_method = db.Column(db.String(50), default='standard')
    shipping_cost = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'total_amount': self.total_amount,
            'order_status': self.order_status,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat(),
            'items': [item.to_dict() for item in self.order_items]
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price at time of order
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': self.price,
            'total': self.quantity * self.price
        }

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'total': self.quantity * self.product.price
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User')
    product = db.relationship('Product', backref='reviews')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user.username,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat()
        }

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Nullable for guest users
    session_id = db.Column(db.String(100), nullable=False)  # For tracking guest sessions
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User')
    
    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'response': self.response,
            'created_at': self.created_at.isoformat()
        }


class LoyaltyPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    points = db.Column(db.Integer, default=0)
    lifetime_points = db.Column(db.Integer, default=0)
    tier = db.Column(db.String(20), default='bronze')  # bronze, silver, gold, platinum
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='loyalty', uselist=False)
    
    # Tier thresholds
    TIER_THRESHOLDS = {
        'bronze': 0,
        'silver': 500,
        'gold': 1500,
        'platinum': 5000
    }
    
    def add_points(self, amount, reason='purchase'):
        """Add points and update tier"""
        if self.points is None:
            self.points = 0
        if self.lifetime_points is None:
            self.lifetime_points = 0
        self.points += amount
        self.lifetime_points += amount
        self.update_tier()
        
        # Create transaction record
        transaction = LoyaltyTransaction(
            loyalty_id=self.id,
            points=amount,
            type='earned',
            reason=reason
        )
        db.session.add(transaction)
        db.session.commit()
        return self.points
    
    def redeem_points(self, amount, reason='redeem'):
        """Redeem points if sufficient balance"""
        if self.points is None:
            self.points = 0
        if self.points >= amount:
            self.points -= amount
            
            transaction = LoyaltyTransaction(
                loyalty_id=self.id,
                points=-amount,
                type='redeemed',
                reason=reason
            )
            db.session.add(transaction)
            db.session.commit()
            return True
        return False
    
    def update_tier(self):
        """Update membership tier based on lifetime points"""
        for tier, threshold in sorted(self.TIER_THRESHOLDS.items(), key=lambda x: x[1], reverse=True):
            if self.lifetime_points >= threshold:
                self.tier = tier
                break
    
    def get_tier_benefits(self):
        """Get benefits for current tier"""
        benefits = {
            'bronze': {'discount': 0, 'points_multiplier': 1, 'free_shipping_threshold': 4150},
            'silver': {'discount': 5, 'points_multiplier': 1.25, 'free_shipping_threshold': 3000},
            'gold': {'discount': 10, 'points_multiplier': 1.5, 'free_shipping_threshold': 2000},
            'platinum': {'discount': 15, 'points_multiplier': 2, 'free_shipping_threshold': 0}
        }
        return benefits.get(self.tier, benefits['bronze'])
    
    def to_dict(self):
        return {
            'id': self.id,
            'points': self.points,
            'lifetime_points': self.lifetime_points,
            'tier': self.tier,
            'tier_name': self.tier.title(),
            'benefits': self.get_tier_benefits(),
            'next_tier': self.get_next_tier_info(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def get_next_tier_info(self):
        """Get information about next tier"""
        tiers = ['bronze', 'silver', 'gold', 'platinum']
        if self.tier in tiers:
            current_idx = tiers.index(self.tier)
            if current_idx < len(tiers) - 1:
                next_tier = tiers[current_idx + 1]
                threshold = self.TIER_THRESHOLDS[next_tier]
                points_needed = threshold - self.lifetime_points
                return {
                    'name': next_tier.title(),
                    'points_needed': max(0, points_needed),
                    'threshold': threshold
                }
        return None


class LoyaltyTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loyalty_id = db.Column(db.Integer, db.ForeignKey('loyalty_points.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False)  # Positive for earned, negative for redeemed
    type = db.Column(db.String(20), nullable=False)  # earned, redeemed, bonus
    reason = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    loyalty = db.relationship('LoyaltyPoints', backref='transactions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'points': self.points,
            'type': self.type,
            'reason': self.reason,
            'created_at': self.created_at.isoformat()
        }


# ============= NEW FEATURES: Wishlist, Recommendations, Multilingual Support =============

class Wishlist(db.Model):
    """User wishlist for saving favorite products"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User')
    product = db.relationship('Product', backref='wishlist_items')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_user_product'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict(),
            'added_at': self.added_at.isoformat()
        }


class ProductRecommendation(db.Model):
    """AI-powered product recommendations"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    score = db.Column(db.Float, default=0.0)  # Recommendation score 0-1
    reason = db.Column(db.String(200), nullable=True)  # Why it's recommended
    recommendation_type = db.Column(db.String(50), nullable=True)  # based_on_category, based_on_history, trending, etc
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)  # Recommendation may expire
    
    # Relationships
    user = db.relationship('User')
    product = db.relationship('Product')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict(),
            'score': self.score,
            'reason': self.reason,
            'type': self.recommendation_type
        }


class UserLanguagePreference(db.Model):
    """Store user's language preference for multilingual support"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    language_code = db.Column(db.String(10), default='en')  # en, hi, or (Odia), etc
    preferred_language_name = db.Column(db.String(50), default='English')
    timezone = db.Column(db.String(50), default='UTC')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='language_preference', uselist=False)
    
    SUPPORTED_LANGUAGES = {
        'en': {'name': 'English', 'native': 'English'},
        'hi': {'name': 'Hindi', 'native': 'हिंदी'},
        'or': {'name': 'Odia', 'native': 'ଓଡ଼ିଆ'},
        'ta': {'name': 'Tamil', 'native': 'தமிழ்'},
        'te': {'name': 'Telugu', 'native': 'తెలుగు'},
        'bn': {'name': 'Bengali', 'native': 'বাংলা'},
        'mr': {'name': 'Marathi', 'native': 'मराठी'},
        'gu': {'name': 'Gujarati', 'native': 'ગુજરાતી'},
    }
    
    def to_dict(self):
        return {
            'id': self.id,
            'language_code': self.language_code,
            'language_name': self.preferred_language_name,
            'timezone': self.timezone,
            'available_languages': self.SUPPORTED_LANGUAGES
        }


class MultilingualChatMessage(db.Model):
    """Enhanced chat messages with multilingual support"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    session_id = db.Column(db.String(100), nullable=False)
    language_code = db.Column(db.String(10), default='en')
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(50), nullable=True)  # product_search, order_status, account, etc
    confidence = db.Column(db.Float, default=0.0)  # Confidence score 0-1
    was_helpful = db.Column(db.Boolean, nullable=True)  # User feedback
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User')
    
    INTENT_TYPES = [
        'product_search',
        'product_recommendation', 
        'order_status',
        'cart_management',
        'account',
        'shipping',
        'payments',
        'returns',
        'general'
    ]
    
    def to_dict(self):
        return {
            'id': self.id,
            'language': self.language_code,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'intent': self.intent,
            'confidence': self.confidence,
            'helpful': self.was_helpful,
            'created_at': self.created_at.isoformat()
        }


class ChatbotIntentClassification(db.Model):
    """Store common intents and their training data for the chatbot"""
    id = db.Column(db.Integer, primary_key=True)
    intent_name = db.Column(db.String(50), unique=True, nullable=False)
    intent_description = db.Column(db.Text, nullable=True)
    example_questions = db.Column(db.Text, nullable=True)  # JSON array of examples
    response_template = db.Column(db.Text, nullable=True)  # Template for bot response
    requires_product_id = db.Column(db.Boolean, default=False)
    requires_user_id = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'intent_name': self.intent_name,
            'description': self.intent_description,
            'examples': json.loads(self.example_questions or '[]'),
            'priority': self.priority,
            'is_active': self.is_active
        }


class NotificationPreference(db.Model):
    """User notification preferences for multilingual support"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    email_notifications = db.Column(db.Boolean, default=True)
    sms_notifications = db.Column(db.Boolean, default=False)
    push_notifications = db.Column(db.Boolean, default=True)
    notification_language = db.Column(db.String(10), default='en')
    order_updates = db.Column(db.Boolean, default=True)
    promotional = db.Column(db.Boolean, default=True)
    weekly_recommendations = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='notification_preferences', uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email_notifications': self.email_notifications,
            'sms_notifications': self.sms_notifications,
            'push_notifications': self.push_notifications,
            'notification_language': self.notification_language,
            'order_updates': self.order_updates,
            'promotional': self.promotional,
            'weekly_recommendations': self.weekly_recommendations
        }

