#!/usr/bin/env python3
"""
Enhanced Chatbot Service for Cartify
Real-world scenarios, more attractive responses, and improved functionality
"""

from models import db, MultilingualChatMessage, Product, Order, User, CartItem, Review
from datetime import datetime, timedelta
import json
import re

class EnhancedChatbot:
    def __init__(self):
        self.context = {}
        self.user_id = None
        self.session_id = None
        
        # Real-world scenarios and responses
        self.scenarios = {
            'greeting': {
                'en': [
                    "👋 Hello! Welcome to Cartify! 🛍️",
                    "Hi there! Ready to find amazing products today? ✨",
                    "Welcome back! What can I help you discover today? 🎯"
                ],
                'hi': [
                    "नमस्ते! Cartify में आपका स्वागत है। 🛍️",
                    "नमस्तक! आज आज क्या ढूंढ रहे है? 🎯"
                ],
                'or': [
                    "ନମସ୍କାର! Cartify ରେ ସାହାଯ୍ଟ କରିପାରେ। 🛍️",
                    "ନମସ୍କାର! ଆପଣାଙ୍କୁ ଉତ୍ପାଦ ଖୋଜିବାରେ? 🎯"
                ],
                'ta': [
                    "வணக்கு ம்! Cartify-க்கு வரேற்கிறோம். 🛍️",
                    "வணக்கு ம்! இன்று தேடுக்கு வரேற்கிறோம்? 🎯"
                ]
            },
            'product_search': {
                'en': [
                    "🔍 I'll help you find the perfect product! What category interests you?",
                    "Let me search for you! Electronics, Fashion, Home, Beauty, Sports... What's your preference? 🛍️",
                    "I can search by name, brand, price range, or features. What would you like? 🎯"
                ],
                'hi': [
                    "🔍 मैं आपको ढूंढ रहे हूँ! कौन सा ढूंढ रहे है? 🛍️",
                    "मैं आपके लिए खोज सकता हूँ! ब्रांड, कैटगरी, मूल्य... क्या चाहिए? 🎯"
                ],
                'or': [
                    "🔍 ମୁଁ ଆପଣଙ୍କୁ ଖୋଜିବାରେ! କୌଣିବାରେ ଖୋଜିବାରେ? 🛍️",
                    "🔍 ମୁଁ ଆପଣଙ୍କୁ ଖୋଜିବାରେ! କୌଣିବାରେ ଖୋଜିବାରେ? 🎯"
                ],
                'ta': [
                    "🔍 நீங்கள் உங்கு ம்! என்னற்கிறோம் தேடுக்கு வரேற்கிறோம். 🛍️",
                    "🔍 பொருட்கள் இருப்பிலுள்ளது! மின்னிற்கிறோம் தேடுக்கு வரேற்கிறோம். 🛍️"
                ]
            },
            'order_tracking': {
                'en': [
                    "📦 Let me check your order status! Please provide your order number. 🕵️",
                    "I'll help you track your package! What's your order ID? 📮",
                    "Let's find your order! I can check status, delivery date, and tracking details. 🚚"
                ],
                'hi': [
                    "📦 आपके ऑर्डर की स्थिति की जांच करने दीजिए। कृपया ऑर्डर नंबर दीजिए। 🕵️",
                    "📦 मैं आपके ऑर्डर की जानकारी देख सकता हूँ! कृपया ऑर्डर नंबर दीजिए। 📮"
                ],
                'or': [
                    "📦 ମୁଁ ଆପଣଙ୍କୁ ଖୋଜିବାରେ! ଆପଣଙ୍କୁ ଖୋଜିବାରେ ଖୋଜିବାରେ? 🕵️",
                    "📦 ମୁଁ ଆପଣଙ୍କୁ ଖୋଜିବାରେ! ଆପଣଙ୍କୁ ଖୋଜିବାରେ ଖୋଜିବାରେ? 📮"
                ],
                'ta': [
                    "📦 உங்கள் ஆர்டர் நிலை சரிப்பிலுள்ளது! ஆர்டர் எண்ணை சரிப்பிலுள்ளது. 🕵️",
                    "📦 உங்கள் ஆர்டர் நிலை சரிப்பிலுள்ளது! ஆர்டர் எண்ணை சரிப்பிலுள்ளது. 📮"
                ]
            },
            'cart_management': {
                'en': [
                    "🛒 Your cart is looking a bit empty! Let me show you some amazing deals! 🎉",
                    "I can help you manage your cart! Add items, remove items, or checkout. What would you like? 🛍️",
                    "Let's optimize your cart! I can suggest alternatives and find discounts for you. 💰"
                ],
                'hi': [
                    "🛒 आपकी कार्ट थोड़ी खाली है! कुछ सामान जोड़ दीजिए। 🎉",
                    "🛒 मैं आपकी कार्ट मैनेज कर सकता हूँ! आइटम जोड़ दीजिए। 🛍️"
                ],
                'or': [
                    "🛒 ଆପଣଙ୍କୁ ଖୋଜିବାରେ! ଆପଣଙ୍କୁ ଖୋଜିବାରେ ଖୋଜିବାରେ! 🎉",
                    "🛒 ଆପଣଙ୍କୁ ଖୋଜିବାରେ! ଆପଣଙ୍କୁ ଖୋଜିବାରେ ଖୋଜିବାରେ! 🎉"
                ],
                'ta': [
                    "🛒 உங்கள் கார்ட் வெறும் சிறும்! சிறும் சேர்து. 🎉",
                    "🛒 உங்கள் கார்ட் வெறும்! சிறும் சேர்து. 🛍️"
                ]
            },
            'payment_help': {
                'en': [
                    "💳 Payment options: Cards, UPI, Net Banking, COD! 💳",
                    "I'll help you with payment! Debit cards, credit cards, UPI, wallets... What do you prefer? 💰",
                    "Secure checkout with multiple payment methods! Easy and safe transactions guaranteed. 🔒"
                ],
                'hi': [
                    "💳 भुगतान के विकल्प: कार्ड, UPI, नेट बैंकिंग, COD! 💳",
                    "💳 मैं आपके लिए भुगता कर सकता हूँ! डेबिट कार्ड, UPI, वॉलेट... क्या पसंद करते हैं? 💰"
                ],
                'or': [
                    "💳 ଭୁକରଭର: କାରରା, UPI, ନେଟ ବ୍ରାଙାରାରା! 💳",
                    "💳 ଭୁକରଭର: କାରରା, UPI, ନେଟ ବ୍ରାଙାରାରା! 💳"
                ],
                'ta': [
                    "💳 கடைய வழங்கு முறைகள்: காட், UPI, நெட் வங்கள் COD! 💳",
                    "💳 உங்கள் கடைய வழங்கு முறைகள்! காட், UPI, நெட் வங்கள்... என்னற்கிறோம்? 💰"
                ]
            },
            'shipping_delivery': {
                'en': [
                    "🚚 Express delivery available! Get your items in 2-3 days! ⚡",
                    "Free shipping on orders above ₹4,150! Standard delivery 5-7 days. 📦",
                    "Track your package in real-time! Get SMS updates on delivery status. 📱"
                ],
                'hi': [
                    "🚚 एक्सप्रेस डिलीवरी उपलब्ध है! 2-3 दिन में पाएं। ⚡",
                    "🚚 ₹4,150 से अधिक ऑर्डर पर मुफ्त शिपिंग! स्टैंडर्ड डिलीवरी 5-7 दिन। 📦"
                ],
                'or': [
                    "🚚 ଏକସପ୍ରିବାରି ଉପଲିବାରେ! 2-3 ଦିନେ ଭିତମାରେ. ⚡",
                    "🚚 ଟ୍ତମାରି ଉପଲିବାରେ! ଏକସପ୍ରିବାରେ ଭିତମାରେ 5-7 ଦିନେ. 📦"
                ],
                'ta': [
                    "🚚 வேகன டிரை உள்ளது! 2-3 நாட்களில் பொருட்கு வரேற்கிறோம். ⚡",
                    "🚚 ரூ.4,150-க்கு மேல் இலவாய ஷிப்பிங்! ஸ்டாண்டிரை டிரை 5-7 நாட்களில். 📦"
                ]
            },
            'returns_refunds': {
                'en': [
                    "🔄 Easy 30-day returns! No questions asked. ✅",
                    "Full refund if you're not satisfied! Hassle-free process guaranteed. 💰",
                    "Return policy: Items must be unused with original packaging. Quick refunds within 5-7 days. 🔄"
                ],
                'hi': [
                    "🔄 30 दिन की आसान रिटर्न पॉलिसी! कोई सवाल नहीं। ✅",
                    "🔄 पूरी तुष्ट होने पर पूरा रिफंड! 5-7 दिन में तुरंत रिफंड। 💰"
                ],
                'or': [
                    "🔄 30 ଦିନେ ପରାରି! କୌଣିବାରେ ବାରି ନାଇ ନାଇ. ✅",
                    "🔄 ପୂର ଟିଣାଙ୍କୁ ଫଳିବାରେ! 5-7 ଦିନେ ଭିତମାରେ ତୁରିଫଳିବାରେ. 💰"
                ],
                'ta': [
                    "🔄 30 நாட்கள் திரும்பிலுள்து! கேட்ட வினற்கிறோம். ✅",
                    "🔄 முழுத்தல் பொருட்கு வரேற்கிறோம்! 5-7 நாட்களில் திரும்பிலுள்து. 💰"
                ]
            },
            'recommendations': {
                'en': [
                    "🎯 Based on your recent views, you might like these products! 🛍️",
                    "Customers who bought this also loved! Personalized recommendations just for you. ⭐",
                    "Trending in your category! These items are popular right now. 🔥"
                ],
                'hi': [
                    "🎯 आपके हाल के आधार पर, यह उत्पाद सकता हूँ! 🛍️",
                    "🎯 जिन आपने देखा, आपको यह पसंद कर सकता हूँ! ⭐",
                    "🎯 आपके पसंद के आधार पर यह भी लोग रहे हैं! 🔥"
                ],
                'or': [
                    "🎯 ଆପଣଙ୍କୁ ଖୋଜିବାରେ! ଆପଣଙ୍କୁ ଖୋଜିବାରେ ଉତ୍ପାଦ ପାରେ କରା! 🛍️",
                    "🎯 ଆପଣଙ୍କୁ ଖୋଜିବାରେ! ଆପଣଙ୍କୁ ଖୋଜିବାରେ ଉତ୍ପାଦ ପାରେ କରା! ⭐",
                    "🎯 ଆପଣଙ୍କୁ ଖୋଜିବାରେ! ଆପଣଙ୍କୁ ଖୋଜିବାରେ ଉତ୍ପାଦ ପାରେ କରା! 🔥"
                ],
                'ta': [
                    "🎯 உங்கள் பார்வுகிறோம், இது தேடுக்கு வரேற்கிறோம்! 🛍️",
                    "🎯 நீங்கள் பார்வுகிறோம், இது தேடுக்கு வரேற்கிறோம்! ⭐",
                    "🎯 உங்கள் பார்வுகிறோம், இது தேடுக்கு வரேற்கிறோம்! 🔥"
                ]
            },
            'support_help': {
                'en': [
                    "🛠️ 24/7 Customer Support! Always here to help you. 📞",
                    "Need help? Contact us at support@cartify.com or use live chat! 💬",
                    "Technical issues? Our experts are ready to assist! 🧰"
                ],
                'hi': [
                    "🛠️ 24/7 ग्राहक समर्थन! हमेशा हमेशा आपकी मदद करने के लिए तैयार हैं। 📞",
                    "🛠️ मदद की जरूरत है? support@cartify.com पर संपर्क करें। 💬",
                    "🛠️ तकनीकी समस्या? हमारे विशेषज आपकी मदद करेंगे। 🧰"
                ],
                'or': [
                    "🛠️ 24/7 ସହାରି ସମର୍ଥ! ସବଦାରି ଆପଣଙ୍କୁ ଖୋଜିବାରେ କରା! 📞",
                    "🛠️ ସହାରି ସମର୍ଥ! support@cartify.com ରେ ସଂପରକରା କରା. 💬",
                    "🛠️ କୌଣିବାରେ? ଆମାଙ୍କୁ ବିରଭରା ଆପଣଙ୍କୁ ଖୋଜିବାରେ କରା! 🧰"
                ],
                'ta': [
                    "🛠️ 24/7 வாணரவு உதவி! உங்கள் உங்கள் முறைகள் தேடுக்கு வரேற்கிறோம். 📞",
                    "🛠️ உதவி வேணருகிறோம்? support@cartify.com ல் தொடங்கு வரேற்கிறோம். 💬",
                    "🛠️ �தொழல் பிரச்சா? ஆமாங்கள் உங்கள் நிபர்வு உதவி வேணருகிறோம். 🧰"
                ]
            },
            'offers_deals': {
                'en': [
                    "🎉 Flash Sale! Up to 50% off on selected items! ⚡",
                    "🔥 Hot Deals! Limited time offers on trending products! 🔥",
                    "💰 Special Discount! Use code SAVE20 for extra 20% off! 🎫",
                    "🎁 Bundle Offers! Buy 2 get 1 free on selected items! 🎁"
                ],
                'hi': [
                    "🎉 फ्लैश सेल! चयनित उत्पाद पर 50% तक छूट! ⚡",
                    "🔥 हॉट डील! सीमित उत्पाद पर समय छूट! 🔥",
                    "💰 खास छूट! कोड SAVE20 उपयोग करें और अतिरिक छूट पाएं! 🎫"
                ],
                'or': [
                    "🎉 ଫ୍ଲାି ବିଲ! ଚୟନିବାରେ 50% ଛୂଟ! ⚡",
                    "🔥 ହଟ୍ ଡିଲ! ନିରବାରେ ଉତ୍ପାଦ ପାରେ ସମିବାରେ! 🔥",
                    "💰 ବିଶିପା! କୋଡ୍ SAVE20 ବ୍ୟିପାରେ କରାବିଲାରେ ଅତିରିପା! 🎫"
                ],
                'ta': [
                    "🎉 விரைப்பு விறோம்! தேர்டுத்த உத்பாத 50% தள்ளது! ⚡",
                    "🔥 ஹாட்ட டீல்! தேர்டுத்த உத்பாத சிறும் சேர்து! 🔥",
                    "💰 சிறும் தள்ளது! SAVE20 கோட் உத்பாத சிறும் சேர்து! 🎫"
                ]
            }
        }
    
    def get_response(self, scenario_key, language='en', context=None):
        """Get contextual response based on scenario and language"""
        if scenario_key in self.scenarios and language in self.scenarios[scenario_key]:
            responses = self.scenarios[scenario_key][language]
            # Return a random response from the list for variety
            import random
            return random.choice(responses)
        return self._get_fallback_response(language, 'general_help')
    
    def _get_fallback_response(self, language='en'):
        """Get fallback response when scenario is not recognized"""
        fallbacks = {
            'en': "I'm here to help! I can assist with products, orders, payments, and support. Ask me anything! 🛍️",
            'hi': "मैं यहां कर सकता हूँ! उत्पाद, ऑर्डर, भुगतान, और समर्थन के लिए मदद कर सकता हूँ। 🛍️",
            'or': "ମୁଁ ଆପଣଙ୍କୁ ଖୋଜିବାରେ! ମେରା, ଆର୍ଡର, ଶିପରା, ଏବଂ ଆଦାରେ ବିରା! 🛍️",
            'ta': "உங்கள் உங்கு ம்! பொருட்கள், ஆர்டர், டெலிவரி, கட்டணம் மற்பும். என்னற்கிறோம். 🛍️"
        }
        return fallbacks.get(language, fallbacks['en'])
    
    def extract_entities(self, message):
        """Extract entities from user message"""
        entities = {
            'product_names': [],
            'categories': [],
            'price_ranges': [],
            'brands': [],
            'order_numbers': [],
            'quantities': [],
            'colors': [],
            'sizes': []
        }
        
        # Product names and brands
        product_keywords = [
            'iphone', 'samsung', 'macbook', 'ipad', 'laptop', 'headphones', 'camera', 
            'watch', 'shoes', 'shirt', 'jacket', 'dress', 'pants', 'jeans',
            'tv', 'refrigerator', 'washing machine', 'vacuum', 'blender', 'coffee maker',
            'மொபன்', 'காட்', 'ஜாமி', 'வேற்பு', 'டீல்', 'சட்டை', 'பாட்'
        ]
        
        # Categories
        categories = [
            'electronics', 'clothing', 'fashion', 'home & garden', 'beauty', 'health',
            'sports', 'outdoors', 'books', 'media', 'toys', 'games', 'automotive',
            'ఎలక్ట్లు', 'దుస్తో', 'ఆహారాయం', 'క్రలు', 'పుస్తో',
            'इலेक்டர்', 'வீட்டர்', 'வீட்டர்', 'விளைக்கு', 'பொருட்கு', 'காட்', 'விளைக்கு',
            'ଇଲେଟର', 'ଭିରା', 'ଖେଲ', 'ଖେଲ', 'ଖେଲ', 'ଖେଲ', 'ଖେଲ', 'ଖେଲ'
        ]
        
        # Price indicators
        price_patterns = [
            (r'under\s*(\d+)', r'above\s*(\d+)', r'between\s*(\d+)\s*and\s*(\d+)', 
            r'cheap', r'expensive', r'affordable', r'budget', r'premium')
        ]
        
        # Order numbers
        order_pattern = r'(?:order|ord|ord)(?:\s*|#)?\s*(\d+)'
        
        message_lower = message.lower()
        
        # Extract products/brands
        for keyword in product_keywords:
            if keyword in message_lower:
                entities['product_names'].append(keyword)
        
        # Extract categories
        for category in categories:
            if category in message_lower:
                entities['categories'].append(category)
        
        # Extract price ranges
        for pattern in price_patterns:
            matches = re.findall(pattern, message_lower)
            if matches:
                entities['price_ranges'].extend(matches)
        
        # Extract order numbers
        order_matches = re.findall(order_pattern, message_lower)
        if order_matches:
            entities['order_numbers'].extend(order_matches)
        
        # Extract quantities
        quantity_patterns = [r'(\d+)\s*(?:piece|pc|item|unit|qty|quantity)']
        for pattern in quantity_patterns:
            matches = re.findall(pattern, message_lower)
            if matches:
                entities['quantities'].extend(matches)
        
        return entities
    
    def get_product_suggestions(self, entities, language='en'):
        """Get product suggestions based on extracted entities"""
        suggestions = []
        
        if entities['categories']:
            for category in entities['categories'][:3]:  # Limit to 3 suggestions
                # Get products from this category
                products = Product.query.filter(
                    Product.category.ilike(f'%{category}%'),
                    Product.is_active == True
                ).limit(5).all()
                
                for product in products:
                    suggestions.append({
                        'name': product.name,
                        'price': f"₹{product.price:,.0f}",
                        'category': product.category,
                        'rating': f"⭐ {product.rating:.1f}",
                        'url': f"/product/{product.id}"
                    })
        
        return suggestions
    
    def get_order_status(self, order_numbers, language='en'):
        """Get order status information"""
        if not order_numbers:
            return self._get_fallback_response(language, 'order_status')
        
        results = []
        for order_num in order_numbers[:3]:  # Limit to 3 orders
            try:
                # Extract numeric part
                numeric_order = re.search(r'\d+', order_num).group()
                if numeric_order:
                    order = Order.query.filter(
                        Order.order_number.ilike(f'%{numeric_order.group()}%')
                    ).first()
                    
                    if order:
                        status_emoji = {
                            'pending': '⏳',
                            'processing': '🔄',
                            'shipped': '🚚',
                            'delivered': '✅',
                            'cancelled': '❌'
                        }
                        
                        results.append({
                            'order_number': order.order_number,
                            'status': order.order_status,
                            'status_emoji': status_emoji.get(order.order_status, '📦'),
                            'total_amount': f"₹{order.total_amount:,.0f}",
                            'items': f"{len(order.order_items)} items",
                            'delivery_date': order.created_at.strftime('%Y-%m-%d') if order.created_at else 'Unknown'
                        })
            except Exception as e:
                continue
        
        return results
    
    def get_cart_info(self, user_id, language='en'):
        """Get user cart information"""
        try:
            cart_items = CartItem.query.filter_by(user_id=user_id).all()
            
            if not cart_items:
                return self.get_response('cart_empty', language)
            
            total_items = len(cart_items)
            total_amount = sum(item.quantity * item.product.price for item in cart_items)
            
            cart_info = {
                'total_items': total_items,
                'total_amount': f"₹{total_amount:,.0f}",
                'items': []
            }
            
            for item in cart_items[:5]:  # Show first 5 items
                cart_info['items'].append({
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'price': f"₹{item.product.price:,.0f}",
                    'total': f"₹{item.quantity * item.product.price:,.0f}"
                })
            
            return cart_info
            
        except Exception as e:
            return self._get_fallback_response(language, 'general_help')
    
    def process_message(self, message, user_id=None, session_id=None, language='en'):
        """Main message processing with enhanced context awareness"""
        # Extract entities
        entities = self.extract_entities(message)
        
        # Detect intent based on entities
        intent = 'general_help'
        
        if any(entity in entities['product_names'] for entity in entities['product_names']):
            intent = 'product_search'
        elif entities['categories']:
            intent = 'product_search'
        elif entities['order_numbers']:
            intent = 'order_tracking'
        elif any(word in message.lower() for word in ['cart', 'basket', 'bag']):
            intent = 'cart_management'
        elif any(word in message.lower() for word in ['pay', 'payment', 'checkout', 'buy']):
            intent = 'payment_help'
        elif any(word in message.lower() for word in ['ship', 'delivery', 'shipping']):
            intent = 'shipping_delivery'
        elif any(word in message.lower() for word in ['return', 'refund', 'exchange']):
            intent = 'returns_refunds'
        elif any(word in message.lower() for word in ['offer', 'deal', 'discount', 'sale']):
            intent = 'offers_deals'
        elif any(word in message.lower() for word in ['recommend', 'suggest', 'similar']):
            intent = 'recommendations'
        elif any(word in message.lower() for word in ['help', 'support', 'issue', 'problem']):
            intent = 'support_help'
        
        # Generate response based on intent
        if intent == 'product_search':
            suggestions = self.get_product_suggestions(entities, language)
            if suggestions:
                response = self.get_response(intent, language)
                response += "\n\n🔍 **Top Suggestions:**\n"
                for i, suggestion in enumerate(suggestions, 1):
                    response += f"{i}. **{suggestion['name']}** - {suggestion['price']} - {suggestion['rating']} - [View Product]({suggestion['url']})\n"
                return response
            else:
                return self.get_response('not_found', language)
        
        elif intent == 'order_tracking':
            order_results = self.get_order_status(entities['order_numbers'], language)
            if order_results:
                response = self.get_response(intent, language)
                response += "\n\n📦 **Order Status:**\n"
                for result in order_results:
                    response += f"• **Order {result['order_number']}** - {result['status_emoji']} {result['status']}\n"
                    response += f"  Amount: {result['total_amount']} | Items: {result['items']} | Date: {result['delivery_date']}\n"
                return response
            else:
                return self.get_response('not_found', language)
        
        elif intent == 'cart_management':
            if user_id:
                cart_info = self.get_cart_info(user_id, language)
                return f"🛒 **Your Cart:**\n{cart_info['total_items']} items | Total: {cart_info['total_amount']}\n\n**Items:**\n" + \
                       "\n".join([f"• {item['name']} - {item['quantity']} pcs - {item['price']} (Total: {item['total']})" for item in cart_info['items']])
            else:
                return self.get_response('greeting', language)
        
        elif intent == 'payment_help':
            return self.get_response(intent, language)
        
        elif intent == 'shipping_delivery':
            return self.get_response(intent, language)
        
        elif intent == 'returns_refunds':
            return self.get_response(intent, language)
        
        elif intent == 'offers_deals':
            return self.get_response(intent, language)
        
        elif intent == 'recommendations':
            return self.get_response(intent, language)
        
        elif intent == 'support_help':
            return self.get_response(intent, language)
        
        else:
            return self.get_response(intent, language)

# Enhanced chatbot instance
enhanced_chatbot = EnhancedChatbot()
