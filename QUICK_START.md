# Quick Start Guide - Cartify with New Features

## 🚀 Getting Started in 5 Minutes

### Step 1: Install & Setup (1 minute)

```bash
# Navigate to project directory
cd d:\zooma\Cartify\Cartify

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### Step 2: Access the Application (30 seconds)

Open your browser and go to:
```
http://localhost:5000
```

### Step 3: Login with Demo Account (30 seconds)

**Demo User Credentials:**
- Username: `demo`
- Password: `demo123`

**Admin Credentials (for management):**
- Username: `admin`
- Password: `admin123`

---

## 🎯 Feature Quick Tour

### 1. Multilingual Chatbot

1. Look for the **floating chat bubble** (bottom-right corner)
2. Click to open the chatbot
3. Select your language from the dropdown
4. Type a question, e.g.:
   - "Find me running shoes"
   - "Show me electronics"
   - "What's trending?"

**Try these in different languages:**

**English:**
- "Find me winter coats"
- "What products do you have?"

**Hindi (हिंदी):**
- "मुझे जूते खोजें"
- "सर्वश्रेष्ठ उत्पाद क्या हैं?"

**Odia (ଓଡ଼ିଆ):**
- "ମୋତେ ଉତ୍ପାଦ ଖୋଜନ୍ତୁ"
- "ଷ୍ଟକରେ ଅଛି?"

### 2. Personalized Recommendations

1. Go to **Recommendations** page (link in navbar)
2. See products recommended just for you
3. View **match scores** for each product
4. Click **Filter buttons** to see different recommendation types
5. Rate recommendations with thumbs up/down

**Recommendation Types:**
- ✅ **Based on Your Category** - Products from categories you like
- 📈 **Similar to Purchases** - Like products you bought
- 🔥 **Trending** - Popular this week
- ⭐ **Top Rated** - Highly reviewed products

### 3. Wishlist Management

1. Click **heart icon** on any product to save
2. Go to **My Wishlist** page
3. See all your saved products
4. **Add to Cart** with one click
5. **Remove** items you don't want
6. Sort by **Add Date**, **Price**, or **Rating**

### 4. Language Settings

1. Go to **Profile** or **Settings**
2. Click **Language Preferences**
3. Select your language:
   - English, Hindi, Odia, Tamil, Telugu, Bengali, Marathi, Gujarati
4. Save preferences (remembered for future visits)

### 5. Notification Preferences

1. Go to **Profile** > **Notifications**
2. Choose what to receive:
   - ✉️ Email Notifications
   - 📱 SMS Notifications
   - 🔔 Push Notifications
3. Select notification types:
   - Order Updates
   - Promotional Offers
   - Weekly Recommendations
4. Save preferences

---

## 🧪 Testing Scenarios

### Test 1: Product Search via Chatbot

1. Open chatbot
2. Keep language as English
3. Type: "Show me electronics under 5000"
4. Chatbot finds matching products
5. Click product to view details

### Test 2: Multilingual Interaction

1. Open chatbot
2. Change language to Hindi
3. Type: "कपड़े दिखाओ" (Show clothes)
4. Get response in Hindi
5. Change to Odia for Odia response

### Test 3: Create Wishlist

1. Browse products page
2. Add 5 products to wishlist ❤️
3. Go to Wishlist page
4. Add some to cart
5. Remove some from wishlist

### Test 4: Get Recommendations

1. Make sure user has purchase history (buy 2-3 items)
2. Go to Recommendations
3. Filter by "Trending"
4. Rate recommendations helpful/not helpful
5. Check recommendations update

### Test 5: Full Checkout Flow

1. Add products via chatbot
2. Navigate to cart
3. Proceed to checkout
4. Enter shipping details
5. Complete payment
6. See order confirmation
7. Ask chatbot about order status

---

## 📊 Admin Dashboard

### Access Admin Features

1. Login as **admin@cartify.com** / **admin123**
2. Go to **Admin Dashboard**
3. Manage:
   - ✅ Products
   - 👥 Users
   - 📦 Orders
   - 💬 Chat Analytics
   - 🎯 Recommendations

### View Chat Statistics

1. Admin Dashboard > **Chat Analytics**
2. See:
   - Total conversations
   - Popular intents
   - Language breakdown
   - Response quality metrics

---

## 🔧 API Testing

### Using cURL

```bash
# Get recommendations
curl http://localhost:5000/api/recommendations

# Get supported languages
curl http://localhost:5000/api/languages/supported

# Send chat message
curl -X POST http://localhost:5000/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{"message":"Find me shoes","language":"en"}'

# Get wishlist
curl http://localhost:5000/api/wishlist
```

### Using Python

```python
import requests

# Chat
response = requests.post('http://localhost:5000/api/chat/send', 
    json={'message': 'Find shoes', 'language': 'en'})
print(response.json())

# Recommendations
response = requests.get('http://localhost:5000/api/recommendations')
print(response.json())

# Wishlist
response = requests.get('http://localhost:5000/api/wishlist')
print(response.json())
```

---

## 📝 Database Information

### SQLite (Default)

- File: `instance/cartify_dev.db`
- No setup needed - created automatically

### MySQL (Optional)

To use MySQL instead of SQLite:

1. Run MySQL setup:
   ```bash
   mysql_setup.bat
   ```

2. Set environment variable:
   ```bash
   set FLASK_ENV=mysql_development
   ```

3. Run app:
   ```bash
   python app.py
   ```

---

## 🎨 UI Highlights

### New Pages

1. **Wishlist** - `/wishlist`
   - Beautiful grid of saved products
   - Price and rating display
   - Add to cart buttons

2. **Recommendations** - `/recommendations`
   - Personalized product suggestions
   - Filter by recommendation type
   - Match score badges
   - Feedback system

3. **Language Settings** - `/profile/language`
   - Choose from 8 languages
   - Set timezone
   - Multilingual UI

### New Components

1. **Floating Chatbot Widget**
   - Always accessible
   - Language selector
   - Message history
   - Gradient design

2. **Wishlist Heart Button**
   - On product cards
   - Toggle saved status
   - Animated feedback

3. **Recommendation Cards**
   - Match score badge
   - Reason for recommendation
   - Quick add to cart
   - Rating display

---

## ⚡ Performance Tips

1. **Enable Caching**:
   ```python
   # In config.py
   CACHE_ENABLED = True
   ```

2. **Optimize Recommendations**:
   - Recommendations refresh every 7 days
   - Cached in database
   - Fast retrieval

3. **Chat Optimization**:
   - Session-based storage
   - Indexed queries
   - Efficient database lookups

---

## 🆘 Troubleshooting

### Chatbot Not Showing

**Solution:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Refresh page (F5)
3. Check browser console for errors (F12)

### Recommendations Not Loading

**Solution:**
1. Ensure user has purchase history
2. Check database connection
3. Verify products exist in database

### Language Not Changing

**Solution:**
1. Try another browser/incognito mode
2. Clear localStorage: `localStorage.clear()`
3. Refresh page

### Database Error

**Solution:**
```bash
# Reset database
del instance/cartify_dev.db
python app.py
```

---

## 📚 Documentation Links

- **Full Features Guide**: [NEW_FEATURES_GUIDE.md](NEW_FEATURES_GUIDE.md)
- **API Documentation**: See `/api/health` for endpoints
- **Database Schema**: Check `models.py`
- **Chatbot Logic**: See `chatbot_service.py`
- **Recommendations**: See `recommendation_service.py`

---

## 🎓 Learning Path

### For Users
1. Create account
2. Browse products
3. Try chatbot in different languages
4. Build wishlist
5. View recommendations
6. Make a purchase

### For Developers
1. Review `models.py` for database schema
2. Study `chatbot_service.py` for NLP logic
3. Check `recommendation_service.py` for ML algorithm
4. Review `api_routes.py` for REST endpoints
5. Test with provided API examples

---

## 📞 Getting Help

1. **Check Documentation**: [NEW_FEATURES_GUIDE.md](NEW_FEATURES_GUIDE.md)
2. **Review Code Comments**: Well-commented source code
3. **Check Error Logs**: Browser console (F12) and Flask logs
4. **Database**: Access SQLite directly or MySQL with client tool

---

## ✅ Checklist for First-Time Users

- [ ] Install dependencies with `pip install -r requirements.txt`
- [ ] Run app with `python app.py`
- [ ] Access at `http://localhost:5000`
- [ ] Login with demo account
- [ ] Open chatbot (bottom-right)
- [ ] Try product search in English
- [ ] Change chatbot language to Hindi
- [ ] Ask question in Hindi
- [ ] Go to Recommendations page
- [ ] Check Wishlist page
- [ ] Update Language Preferences
- [ ] View Notification Settings
- [ ] Browse Admin Dashboard (login as admin)
- [ ] Test API endpoints with cURL/Python
- [ ] Make test purchase
- [ ] Review all files included in package

---

**Enjoy your new Cartify experience! 🎉**

For more help, refer to the comprehensive [NEW_FEATURES_GUIDE.md](NEW_FEATURES_GUIDE.md)
