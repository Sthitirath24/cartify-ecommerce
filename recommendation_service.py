"""
Product Recommendation Engine for Cartify
Generates personalized recommendations based on:
- Purchase history
- Product categories
- Similar product purchases
- Trending products
- Collaborative filtering
"""

from models import db, Product, Order, OrderItem, Review, ProductRecommendation, CartItem, Wishlist
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
import random


class RecommendationEngine:
    """Generates intelligent product recommendations"""
    
    def __init__(self):
        self.recommendation_types = [
            'based_on_category',
            'based_on_history',
            'trending',
            'similar_products',
            'complementary_products',
            'wishlist_related',
            'high_rated'
        ]
    
    def get_user_recommendations(self, user_id, limit=5):
        """Get personalized recommendations for a user"""
        try:
            recommendations = []
            
            # Get user's purchase history
            purchase_history = self._get_purchase_history(user_id)
            
            # Get user's wishlist
            wishlist = self._get_wishlist(user_id)
            
            # Generate recommendations from different sources
            if purchase_history:
                # Category-based recommendations
                category_recs = self._get_category_recommendations(user_id, purchase_history)
                recommendations.extend(category_recs)
                
                # Similar product recommendations
                similar_recs = self._get_similar_product_recommendations(user_id, purchase_history)
                recommendations.extend(similar_recs)
                
                # Complementary products
                comp_recs = self._get_complementary_products(purchase_history)
                recommendations.extend(comp_recs)
            
            # Wishlist-related recommendations
            if wishlist:
                wish_recs = self._get_wishlist_related_recommendations(wishlist)
                recommendations.extend(wish_recs)
            
            # Trending products
            trending_recs = self._get_trending_products(user_id, purchase_history)
            recommendations.extend(trending_recs)
            
            # High-rated products
            high_rated_recs = self._get_high_rated_products(user_id, purchase_history)
            recommendations.extend(high_rated_recs)
            
            # Remove duplicates and sort by score
            seen_products = set()
            unique_recs = []
            for rec in recommendations:
                if rec['product_id'] not in seen_products:
                    seen_products.add(rec['product_id'])
                    unique_recs.append(rec)
            
            # Sort by score and return top recommendations
            unique_recs.sort(key=lambda x: x['score'], reverse=True)
            return unique_recs[:limit]
        
        except Exception as e:
            print(f"Recommendation error: {e}")
            return []
    
    def _get_purchase_history(self, user_id, days=90):
        """Get user's purchase history within last N days"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            orders = Order.query.filter(
                and_(Order.user_id == user_id, Order.created_at >= cutoff_date)
            ).all()
            
            purchased_products = []
            for order in orders:
                for item in order.order_items:
                    purchased_products.append({
                        'product_id': item.product_id,
                        'category': item.product.category,
                        'price': item.product.price,
                        'purchase_date': order.created_at
                    })
            return purchased_products
        except Exception as e:
            print(f"Purchase history error: {e}")
            return []
    
    def _get_wishlist(self, user_id):
        """Get user's wishlist items"""
        try:
            wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()
            return [item.product_id for item in wishlist_items]
        except Exception as e:
            print(f"Wishlist error: {e}")
            return []
    
    def _get_category_recommendations(self, user_id, purchase_history, limit=3):
        """Recommend products from categories user has purchased from"""
        try:
            if not purchase_history:
                return []
            
            categories = list(set([p['category'] for p in purchase_history]))
            purchased_product_ids = [p['product_id'] for p in purchase_history]
            
            recommendations = []
            for category in categories:
                products = Product.query.filter(
                    and_(
                        Product.category == category,
                        Product.id.notin_(purchased_product_ids),
                        Product.is_active == True
                    )
                ).order_by(Product.rating.desc()).limit(limit).all()
                
                for product in products:
                    recommendations.append({
                        'product_id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'category': product.category,
                        'image': product.image_url,
                        'rating': product.rating,
                        'type': 'based_on_category',
                        'reason': f'You liked products in {category}',
                        'score': 0.8 + (product.rating / 5 * 0.2)
                    })
            
            return recommendations
        except Exception as e:
            print(f"Category recommendation error: {e}")
            return []
    
    def _get_similar_product_recommendations(self, user_id, purchase_history, limit=3):
        """Recommend similar products based on purchase history"""
        try:
            if not purchase_history:
                return []
            
            recommendations = []
            purchased_product_ids = [p['product_id'] for p in purchase_history]
            
            # Get products with similar prices and categories
            for purchased in purchase_history[-3:]:  # Look at recent purchases
                price_range = (purchased['price'] * 0.7, purchased['price'] * 1.3)
                
                similar = Product.query.filter(
                    and_(
                        Product.category == purchased['category'],
                        Product.price.between(price_range[0], price_range[1]),
                        Product.id.notin_(purchased_product_ids),
                        Product.is_active == True
                    )
                ).order_by(Product.rating.desc()).limit(limit).all()
                
                for product in similar:
                    recommendations.append({
                        'product_id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'category': product.category,
                        'image': product.image_url,
                        'rating': product.rating,
                        'type': 'based_on_history',
                        'reason': f'Similar to your recent purchases',
                        'score': 0.75 + (product.rating / 5 * 0.25)
                    })
            
            return recommendations
        except Exception as e:
            print(f"Similar product recommendation error: {e}")
            return []
    
    def _get_complementary_products(self, purchase_history, limit=2):
        """Recommend complementary products"""
        try:
            recommendations = []
            
            # Define complementary categories
            complements = {
                'Electronics': ['Accessories', 'Gadgets'],
                'Clothing': ['Shoes', 'Accessories'],
                'Shoes': ['Clothing', 'Socks'],
                'Books': ['Stationery'],
            }
            
            purchased_categories = set([p['category'] for p in purchase_history])
            
            for cat in purchased_categories:
                comp_categories = complements.get(cat, [])
                products = Product.query.filter(
                    and_(
                        Product.category.in_(comp_categories),
                        Product.is_active == True
                    )
                ).order_by(Product.rating.desc()).limit(limit).all()
                
                for product in products:
                    recommendations.append({
                        'product_id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'category': product.category,
                        'image': product.image_url,
                        'rating': product.rating,
                        'type': 'complementary_products',
                        'reason': f'Goes well with {cat}',
                        'score': 0.7 + (product.rating / 5 * 0.3)
                    })
            
            return recommendations
        except Exception as e:
            print(f"Complementary product error: {e}")
            return []
    
    def _get_wishlist_related_recommendations(self, wishlist_ids, limit=2):
        """Recommend products related to wishlist items"""
        try:
            recommendations = []
            
            if not wishlist_ids:
                return []
            
            wishlist_products = Product.query.filter(Product.id.in_(wishlist_ids)).all()
            categories = set([p.category for p in wishlist_products])
            
            products = Product.query.filter(
                and_(
                    Product.category.in_(categories),
                    Product.id.notin_(wishlist_ids),
                    Product.is_active == True
                )
            ).order_by(Product.rating.desc()).limit(limit).all()
            
            for product in products:
                recommendations.append({
                    'product_id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'category': product.category,
                    'image': product.image_url,
                    'rating': product.rating,
                    'type': 'wishlist_related',
                    'reason': 'Related to your wishlist',
                    'score': 0.72
                })
            
            return recommendations
        except Exception as e:
            print(f"Wishlist related error: {e}")
            return []
    
    def _get_trending_products(self, user_id, purchase_history, limit=3):
        """Get trending products across the platform"""
        try:
            purchased_product_ids = [p['product_id'] for p in purchase_history]
            
            # Get products with highest sales in last 30 days
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            trending = db.session.query(
                Product.id,
                Product.name,
                Product.price,
                Product.category,
                Product.image_url,
                Product.rating,
                func.count(OrderItem.id).label('sales_count')
            ).join(
                OrderItem, Product.id == OrderItem.product_id
            ).join(
                Order, OrderItem.order_id == Order.id
            ).filter(
                and_(
                    Order.created_at >= cutoff_date,
                    Product.is_active == True,
                    Product.id.notin_(purchased_product_ids)
                )
            ).group_by(Product.id).order_by(
                func.count(OrderItem.id).desc()
            ).limit(limit).all()
            
            recommendations = []
            for product in trending:
                recommendations.append({
                    'product_id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'category': product.category,
                    'image': product.image_url,
                    'rating': product.rating,
                    'type': 'trending',
                    'reason': 'Trending this week',
                    'score': 0.65 + (product.rating / 5 * 0.35)
                })
            
            return recommendations
        except Exception as e:
            print(f"Trending products error: {e}")
            return []
    
    def _get_high_rated_products(self, user_id, purchase_history, limit=2):
        """Get highly rated products in categories user is interested in"""
        try:
            if not purchase_history:
                return []
            
            categories = list(set([p['category'] for p in purchase_history]))
            purchased_product_ids = [p['product_id'] for p in purchase_history]
            
            products = Product.query.filter(
                and_(
                    Product.category.in_(categories),
                    Product.id.notin_(purchased_product_ids),
                    Product.rating >= 4.0,
                    Product.is_active == True
                )
            ).order_by(Product.rating.desc(), Product.review_count.desc()).limit(limit).all()
            
            recommendations = []
            for product in products:
                recommendations.append({
                    'product_id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'category': product.category,
                    'image': product.image_url,
                    'rating': product.rating,
                    'type': 'high_rated',
                    'reason': f'Highly rated ({product.rating}⭐)',
                    'score': 0.6 + (product.rating / 5 * 0.4)
                })
            
            return recommendations
        except Exception as e:
            print(f"High rated products error: {e}")
            return []
    
    def save_recommendations(self, user_id, recommendations):
        """Save recommendations to database"""
        try:
            # Clear old recommendations
            ProductRecommendation.query.filter_by(user_id=user_id).delete()
            
            for rec in recommendations:
                expires_at = datetime.utcnow() + timedelta(days=7)
                recommendation = ProductRecommendation(
                    user_id=user_id,
                    product_id=rec['product_id'],
                    score=rec['score'],
                    reason=rec['reason'],
                    recommendation_type=rec['type'],
                    expires_at=expires_at
                )
                db.session.add(recommendation)
            
            db.session.commit()
            return True
        except Exception as e:
            print(f"Save recommendations error: {e}")
            db.session.rollback()
            return False


# Create a global recommendation engine instance
recommendation_engine = RecommendationEngine()
