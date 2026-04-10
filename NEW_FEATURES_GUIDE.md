# Cartify E-Commerce Platform - New Features Documentation

## 🎉 What's New in Cartify v2.0

This comprehensive guide covers all the new features added to the Cartify e-commerce platform.

## 📋 Table of Contents

1. [Multilingual Chatbot](#multilingual-chatbot)
2. [Product Recommendations Engine](#product-recommendations-engine)
3. [Wishlist Feature](#wishlist-feature)
4. [Language Support](#language-support)
5. [Notification Preferences](#notification-preferences)
6. [Database Models](#database-models)
7. [API Endpoints](#api-endpoints)
8. [Usage Guide](#usage-guide)
9. [Troubleshooting](#troubleshooting)

---

## 🤖 Multilingual Chatbot

### Features

- **Multi-language Support**: English, Hindi, Odia, Tamil, Telugu, Bengali, Marathi, Gujarati
- **Intent Recognition**: Automatically detects user intent (product search, order status, account, etc.)
- **Natural Conversation**: Contextual responses based on user needs
- **Session Management**: Maintains chat history per user session
- **Feedback System**: Users can rate helpfulness of responses

### Supported Languages

| Code | Language | Native Name |
|------|----------|------------|
| en | English | English |
| hi | Hindi | हिंदी |
| or | Odia | ଓଡ଼ିଆ |
| ta | Tamil | தமிழ் |
| te | Telugu | తెలుగు |
| bn | Bengali | বাংলা |
| mr | Marathi | मराठी |
| gu | Gujarati | ગુજરાતી |

### Intent Types

1. **product_search** - Search for products
2. **order_status** - Track orders
3. **product_recommendation** - Get personalized suggestions
4. **cart_management** - Manage shopping cart
5. **account** - Account-related queries
6. **shipping** - Shipping information
7. **payments** - Payment methods
8. **returns** - Return policies
9. **general** - General conversation

### How to Use

1. Click the floating chatbot icon (bottom right)
2. Select your preferred language from dropdown
3. Type your question or command
4. Get instant response from the bot
5. Add products to cart directly from chat

### Backend Workflow

```
User Message → Language Detection → Intent Classification 
→ Product/Order Lookup → Response Generation → Database Logging
```

---

## 🎯 Product Recommendations Engine

### Features

- **Personalized Recommendations**: Based on purchase history, preferences, and behavior
- **Multiple Recommendation Types**:
  - Based on category preferences
  - Based on purchase history
  - Trending products
  - Similar products
  - Complementary products
  - Wishlist-related items
  - High-rated products

- **Confidence Scoring**: Each recommendation has a match score (0-1)
- **Feedback Loop**: Improves recommendations based on user feedback
- **Expiring Recommendations**: Recommendations refresh every 7 days

### Recommendation Algorithm

1. **Analyze Purchase History** (last 90 days)
2. **Extract User Preferences**:
   - Product categories
   - Price ranges
   - Brands
3. **Generate Recommendations**:
   - Category-based
   - Similar products
   - Trending items
4. **Score & Sort** by relevance
5. **Remove Duplicates**
6. **Return Top N** recommendations

### Recommendation Score Factors

- Product rating (40% weight)
- Relevance to user interests (35% weight)
- Trend & popularity (15% weight)
- User feedback history (10% weight)

---

## ❤️ Wishlist Feature

### Features

- **Save Products**: Add products to personal wishlist
- **Price Tracking**: Get notified when prices drop
- **Move to Cart**: Easy transfer from wishlist to cart
- **Remove Items**: Organize wishlist
- **Sharing**: (Future feature) Share wishlists with friends

### How to Use

1. Browse products
2. Click heart icon to add to wishlist
3. View all wishlist items: `/wishlist`
4. Add items to cart from wishlist
5. Clear wishlist when needed

### Wishlist Information Tracked

- User ID
- Product ID
- Date added
- Product current price
- Product availability

---

## 🌍 Language Support & Preferences

### Features

- **User Language Preference**: Set default language per user
- **Timezone Support**: Store user's timezone
- **Persistent Storage**: Preferences saved to database
- **Multi-Language UI**: App interface translates based on preference

### Language Preference Model

```python
UserLanguagePreference:
- user_id (Foreign Key)
- language_code (en, hi, or, etc.)
- preferred_language_name
- timezone
- updated_at
```

### API Usage

```bash
# Get language preference
GET /api/language/preference

# Set language preference
POST /api/language/preference
{
    "language_code": "hi",
    "timezone": "Asia/Kolkata"
}

# Get supported languages
GET /api/languages/supported
```

---

## 🔔 Notification Preferences

### Features

- **Multi-Channel Notifications**:
  - Email notifications
  - SMS notifications (future)
  - Push notifications

- **Notification Types**:
  - Order updates
  - Promotional offers
  - Weekly recommendations
  - Price drops on wishlist items

- **User Control**: Enable/disable each type

### Notification Preference Model

```python
NotificationPreference:
- user_id (Foreign Key)
- email_notifications (Boolean)
- sms_notifications (Boolean)
- push_notifications (Boolean)
- notification_language
- order_updates (Boolean)
- promotional (Boolean)
- weekly_recommendations (Boolean)
```

---

## 🗄️ Database Models

### New Tables

1. **Wishlist** - User's saved products
2. **ProductRecommendation** - Personalized recommendations
3. **UserLanguagePreference** - Language & timezone settings
4. **MultilingualChatMessage** - Chat history with translations
5. **ChatbotIntentClassification** - Intent training data
6. **NotificationPreference** - User notification settings

### Table Relationships

```
User (1) ──→ (Many) Wishlist
User (1) ──→ (Many) ProductRecommendation
User (1) ──→ (1) UserLanguagePreference
User (1) ──→ (Many) MultilingualChatMessage
User (1) ──→ (1) NotificationPreference
Product (1) ──→ (Many) Wishlist
Product (1) ──→ (Many) ProductRecommendation
```

---

## 📡 API Endpoints

### Chatbot Endpoints

```
POST /api/chat/send
GET /api/chat/history
```

### Wishlist Endpoints

```
POST /api/wishlist/add
DELETE /api/wishlist/remove/<product_id>
GET /api/wishlist
```

### Recommendations Endpoints

```
GET /api/recommendations
POST /api/recommendations/<product_id>/feedback
```

### Language Endpoints

```
GET /api/language/preference
POST /api/language/preference
GET /api/languages/supported
```

### Notification Endpoints

```
GET /api/notifications/preference
POST /api/notifications/preference
```

### Search Endpoint

```
GET /api/search?q=<query>&lang=<language>&category=<category>&limit=<limit>
```

### Health Check

```
GET /api/health
```

---

## 💡 Usage Guide

### For End Users

#### Using the Chatbot

1. **Open Chatbot**: Click the floating chat bubble (bottom-right)
2. **Change Language**: Select from dropdown menu
3. **Ask Questions**:
   - "Find me running shoes"
   - "What's the status of my order?"
   - "Recommend something for me"
4. **Add to Cart**: Click products directly from chat

#### Viewing Recommendations

1. Navigate to **Recommendations** page
2. Filter by type (Trending, Top Rated, etc.)
3. See match scores and reasons
4. Rate recommendation helpfulness
5. Add to cart or wishlist

#### Managing Wishlist

1. Go to **My Wishlist** page
2. Browse saved products
3. Add to cart with one click
4. Remove items as needed
5. Get price drop notifications

### For Developers

#### Adding Chatbot to Templates

```html
{% include 'chatbot_widget.html' %}
```

#### Integrating Recommendations

```python
from recommendation_service import recommendation_engine

# Get recommendations for user
recommendations = recommendation_engine.get_user_recommendations(user_id, limit=5)
```

#### Logging Chat Messages

```python
from chatbot_service import chatbot

# Log a chat interaction
chatbot.log_chat_message(
    user_id=user_id,
    session_id=session_id,
    language='en',
    user_message="Find me shoes",
    bot_response="Here are some shoes...",
    intent='product_search',
    confidence=0.92
)
```

---

## 🔧 Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Update Database

```bash
python
>>> from app import create_tables
>>> create_tables()
```

### 3. Run Application

```bash
python app.py
```

### 4. Initialize Features

New features are automatically initialized on first run:
- Chatbot intents created
- Language preferences set for users
- Notification preferences initialized

---

## 🎨 UI Components

### Chatbot Widget

- Floating chat button (bottom-right)
- Language selector dropdown
- Message history display
- Real-time typing indicators
- Responsive design (mobile/desktop)

### Wishlist Page

- Product grid layout
- Add to cart buttons
- Remove from wishlist
- Browse and compare
- Empty state messaging

### Recommendations Page

- Filter buttons (Category, Trending, etc.)
- Match score badges
- Recommendation reason display
- Feedback buttons
- Responsive grid

---

## 🐛 Troubleshooting

### Chatbot Issues

**Problem**: Chatbot not responding
- **Solution**: Check chatbot service is running, verify database connection

**Problem**: Language not changing
- **Solution**: Clear browser cache, verify language code is supported

### Recommendation Issues

**Problem**: No recommendations showing
- **Solution**: Ensure user has purchase history, check database for products

**Problem**: Slow recommendations
- **Solution**: Limit recommendation queries, use caching

### Wishlist Issues

**Problem**: Can't add to wishlist
- **Solution**: Check user is logged in, verify product exists

**Problem**: Wishlist not loading
- **Solution**: Check database connection, verify API endpoint

---

## 📊 Statistics & Monitoring

### Chat Statistics

- Total chat sessions
- Average response time
- Popular intents
- Language usage breakdown
- Helpful/unhelpful feedback ratio

### Recommendation Metrics

- Recommendation click-through rate
- Add-to-cart conversion rate
- Average match score
- Feedback distribution

### Wishlist Analytics

- Total items saved
- Most-wishlisted products
- Wishlist-to-cart conversion
- Average wishlist size per user

---

## 🚀 Future Enhancements

### Planned Features

1. **Voice Chatbot**: Speech-to-text input
2. **Video Recommendations**: Show product videos
3. **AR Try-On**: Augmented reality product preview
4. **Social Wishlist**: Share wishlists with friends
5. **Price Drop Alerts**: Notify on price changes
6. **Similar Items**: "Customers also liked" section
7. **AI-Powered Descriptions**: Auto-generate product details
8. **Sentiment Analysis**: Analyze review sentiments

---

## 📞 Support

For issues or questions:

1. Check troubleshooting section
2. Review API documentation
3. Check database logs
4. Contact support team

---

## 📄 License

This documentation is part of Cartify E-Commerce Platform.
For licensing details, see LICENSE file.

---

**Version**: 2.0
**Last Updated**: 2024
**Author**: Cartify Development Team
