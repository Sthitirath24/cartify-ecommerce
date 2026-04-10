# Cartify v2.0 - Feature Testing Guide

## ✅ Comprehensive Testing Checklist

This guide helps you verify that all new features are working correctly.

---

## 🧪 Pre-Testing Setup

### 1. Start the Application
```bash
cd d:\zooma\Cartify\Cartify
python app.py
```

Expected: App running on `http://localhost:5000`

### 2. Login with Demo Account
- URL: `http://localhost:5000/login`
- Username: `demo`
- Password: `demo123`

---

## 🤖 Test 1: Multilingual Chatbot

### Test 1.1: Chatbot Interface
- [ ] Floating chat button visible (bottom-right corner)
- [ ] Click to open chatbot widget
- [ ] Widget slides up smoothly
- [ ] Language dropdown shows 8 languages
- [ ] Input field is focused on open
- [ ] Close button (X) closes the widget

### Test 1.2: English Chat
1. Select "English" from dropdown
2. Type: "Find me running shoes"
3. Verify:
   - [ ] Message appears in chat
   - [ ] Bot responds in English
   - [ ] Response mentions products
   - [ ] Typing indicator shows before response

### Test 1.3: Hindi Chat
1. Select "हिंदी" from dropdown
2. Type: "मुझे जूते खोजें"
3. Verify:
   - [ ] Chatbot switches to Hindi
   - [ ] Response is in Hindi
   - [ ] UI text is in Hindi

### Test 1.4: Hindi (Roman) Chat
1. Keep Hindi selected
2. Type: "mujhe jute dikhaiye"
3. Verify:
   - [ ] Product search works in Roman script
   - [ ] Returns products
   - [ ] Response is in Hindi

### Test 1.5: Odia Chat
1. Select "ଓଡ଼ିଆ" 
2. Type: "ମୋତେ ଉତ୍ପାଦ ଖୋଜନ୍ତୁ"
3. Verify:
   - [ ] Response in Odia script
   - [ ] All UI updates to Odia

### Test 1.6: Other Languages
- [ ] Tamil (தமிழ்) works
- [ ] Telugu (తెలుగు) works
- [ ] Bengali (বাংলা) works
- [ ] Marathi (मराठी) works
- [ ] Gujarati (ગુજરાતી) works

### Test 1.7: Chat History
1. Send multiple messages
2. Verify:
   - [ ] All messages appear in order
   - [ ] User messages right-aligned
   - [ ] Bot messages left-aligned
   - [ ] Different colors for user/bot
   - [ ] Timestamp visible

### Test 1.8: Intent Recognition
Try different intents:

**Product Search:**
- [ ] "Find electronics"
- [ ] "Show me clothes under 2000"
- [ ] "What products do you have?"

**Order Status:**
- [ ] "Where's my order?"
- [ ] "Track my order"
- [ ] "Order status"

**Account:**
- [ ] "Update my profile"
- [ ] "Change password"

**General:**
- [ ] "Hello"
- [ ] "Help"

### Test 1.9: Chat Persistence
1. Refresh page
2. Open chatbot
3. Verify:
   - [ ] Chat history is preserved
   - [ ] Session continues

---

## ❤️ Test 2: Wishlist Feature

### Test 2.1: Add to Wishlist
1. Go to `/products`
2. Find any product with heart icon
3. Click heart icon
4. Verify:
   - [ ] Heart fills with color
   - [ ] Confirmation message appears
   - [ ] Product added to wishlist

### Test 2.2: Wishlist Page
1. Go to `/wishlist`
2. Verify:
   - [ ] All added products visible
   - [ ] Product images display
   - [ ] Prices correct
   - [ ] Ratings visible
   - [ ] Review count shown

### Test 2.3: Wishlist Actions
1. On wishlist page:
   - [ ] "Add to Cart" button works
   - [ ] Product moves to cart
   - [ ] Product stays in wishlist

### Test 2.4: Remove from Wishlist
1. Click remove/trash icon
2. Verify:
   - [ ] Product removed
   - [ ] Page updates
   - [ ] Heart icon empty on products page

### Test 2.5: Empty Wishlist
1. Remove all items
2. Verify:
   - [ ] Empty state message shows
   - [ ] "Continue Shopping" link appears
   - [ ] Graceful display

### Test 2.6: Wishlist UI
- [ ] Responsive on mobile (< 600px)
- [ ] Responsive on tablet (600-1024px)
- [ ] Responsive on desktop (> 1024px)
- [ ] All buttons styled correctly
- [ ] Images load properly
- [ ] No layout breaks

---

## 🎯 Test 3: Recommendations

### Test 3.1: Recommendations Page
1. Go to `/recommendations`
2. Verify:
   - [ ] Page loads
   - [ ] Recommendations visible
   - [ ] Products in grid layout
   - [ ] Filter buttons present

### Test 3.2: Recommendation Data
For each card verify:
- [ ] Product image displays
- [ ] Product name visible
- [ ] Price shown
- [ ] Category displayed
- [ ] Rating with stars
- [ ] Match score badge
- [ ] Recommendation reason

### Test 3.3: Filter Buttons
Click each filter:
- [ ] "All" shows all recommendations
- [ ] "Your Category" shows category-based
- [ ] "Similar to Purchases" shows history-based
- [ ] "Trending" shows trending products
- [ ] "Top Rated" shows high-rated products
- [ ] Active button highlights

### Test 3.4: Recommendation Actions
- [ ] "Add to Cart" button works
- [ ] "Wishlist" button works
- [ ] Thumbs up/down feedback works

### Test 3.5: Feedback System
1. Click thumbs up on a recommendation
2. Verify:
   - [ ] Feedback recorded
   - [ ] No page reload
   - [ ] Button shows feedback received

### Test 3.6: Responsive Design
- [ ] Mobile layout (mobile grid 1 col)
- [ ] Tablet layout (2 cols)
- [ ] Desktop layout (3 cols)
- [ ] All buttons accessible on mobile

---

## 🌍 Test 4: Language Preferences

### Test 4.1: Access Language Settings
1. Go to profile/settings
2. Find "Language Preferences" option
3. Verify:
   - [ ] All 8 languages in dropdown
   - [ ] Current language selected
   - [ ] Timezone field present

### Test 4.2: Change Language
1. Select a different language
2. Copy your timezone: "Asia/Kolkata"
3. Click Save
4. Verify:
   - [ ] Confirmation message appears
   - [ ] Language saved
   - [ ] Preferences persist after refresh

### Test 4.3: Supported Languages List
1. API: `GET /api/languages/supported`
2. Verify:
   - [ ] Returns all 8 languages
   - [ ] Includes native names
   - [ ] JSON format correct

---

## 🔔 Test 5: Notification Preferences

### Test 5.1: Access Notifications
1. Go to profile/settings
2. Find "Notification Settings"
3. Verify:
   - [ ] All options visible
   - [ ] Checkboxes functional
   - [ ] Language selector present

### Test 5.2: Notification Types
- [ ] Email notifications toggle
- [ ] SMS notifications toggle
- [ ] Push notifications toggle
- [ ] Order updates toggle
- [ ] Promotional toggle
- [ ] Weekly recommendations toggle

### Test 5.3: Save Preferences
1. Change some settings
2. Click Save
3. Verify:
   - [ ] Confirmation message
   - [ ] Settings saved
   - [ ] Preferences persist

---

## 📡 Test 6: API Endpoints

### Test 6.1: Health Check
```bash
curl http://localhost:5000/api/health
```
Verify: Returns 200 with success message

### Test 6.2: Chat Endpoint
```bash
curl -X POST http://localhost:5000/api/chat/send \
  -H "Content-Type: application/json" \
  -d '{"message":"Find shoes","language":"en"}'
```
Verify: Returns bot response

### Test 6.3: Wishlist Endpoints
```bash
# Get wishlist
curl http://localhost:5000/api/wishlist

# Add to wishlist
curl -X POST http://localhost:5000/api/wishlist/add \
  -H "Content-Type: application/json" \
  -d '{"product_id":1}'
```
Verify: Returns successful responses

### Test 6.4: Recommendations Endpoint
```bash
curl http://localhost:5000/api/recommendations?limit=5
```
Verify: Returns list of recommendations

### Test 6.5: Language Endpoint
```bash
curl http://localhost:5000/api/languages/supported
```
Verify: Returns all 8 languages

### Test 6.6: Search Endpoint
```bash
curl "http://localhost:5000/api/search?q=shoes&lang=en"
```
Verify: Returns products matching query

---

## 🗄️ Test 7: Database

### Test 7.1: Check New Tables
Open SQLite or MySQL client:
```sql
.tables
```
Verify tables exist:
- [ ] wishlist
- [ ] product_recommendation
- [ ] user_language_preference
- [ ] multilingual_chat_message
- [ ] chatbot_intent_classification
- [ ] notification_preference

### Test 7.2: Data Insertion
1. Add item to wishlist
2. Query database:
```sql
SELECT * FROM wishlist WHERE user_id = 1;
```
Verify: Product appears

### Test 7.3: Relationships
```sql
SELECT u.username, w.product_id 
FROM user u 
JOIN wishlist w ON u.id = w.user_id;
```
Verify: User-wishlist relationship works

---

## 🔐 Test 8: Security

### Test 8.1: Authentication
- [ ] Can't access `/recommendations` without login
- [ ] Can't access `/wishlist` without login
- [ ] Can't use `/api/wishlist` without login
- [ ] Login required message shown

### Test 8.2: Data Validation
- [ ] Empty chat messages rejected
- [ ] Invalid product IDs handled
- [ ] SQL injection attempts blocked
- [ ] XSS attempts prevented

### Test 8.3: User Isolation
1. Login as user A, add to wishlist
2. Login as user B
3. Verify:
   - [ ] User B can't see user A's wishlist
   - [ ] User B gets own recommendations
   - [ ] No data leakage

---

## ⚡ Test 9: Performance

### Test 9.1: Load Times
- [ ] Chatbot widget loads instantly
- [ ] Wishlist page < 2 seconds
- [ ] Recommendations page < 2 seconds
- [ ] API response < 500ms

### Test 9.2: Database Queries
- [ ] No N+1 query problems
- [ ] Indexes being used
- [ ] Queries optimized

### Test 9.3: Memory Usage
- App running with reasonable memory
- No memory leaks
- Graceful error handling

---

## 🎨 Test 10: UI/UX

### Test 10.1: Design
- [ ] Consistent color scheme
- [ ] Readable fonts
- [ ] Proper spacing
- [ ] Professional appearance
- [ ] Gradient buttons

### Test 10.2: Animations
- [ ] Smooth transitions
- [ ] Hover effects work
- [ ] No janky animations
- [ ] Loading states visible
- [ ] Typing indicator animates

### Test 10.3: Accessibility
- [ ] Keyboard navigation works
- [ ] Color contrast sufficient
- [ ] Font sizes readable
- [ ] Buttons clickable
- [ ] Touch-friendly buttons (mobile)

---

## 🔄 Test 11: Integration Tests

### Test 11.1: Full Chat Flow
1. Open chatbot
2. Search for product: "shoes"
3. Verify product found
4. Add to cart from chat
5. Verify in cart

### Test 11.2: Full Wishlist Flow
1. Add product to wishlist
2. Go to recommendations
3. Click wishlist button
4. Verify added to wishlist
5. Go to wishlist page
6. Verify product there

### Test 11.3: Full Recommendation Flow
1. Make purchase (add 2-3 items to cart)
2. Checkout
3. Go to recommendations
4. Verify personalized recommendations
5. Add recommendation to wishlist
6. Verify in wishlist

### Test 11.4: Multi-Language Flow
1. Change language to Hindi
2. Open chatbot (should use Hindi)
3. Search in Hindi
4. Change preference to Hindi
5. Verify chat defaults to Hindi next time

---

## 📊 Test 12: Admin Dashboard

### Test 12.1: Access Admin Panel
1. Login as admin@cartify.com / admin123
2. Go to Admin Dashboard
3. Verify:
   - [ ] Dashboard loads
   - [ ] Stats visible
   - [ ] Menu accessible

### Test 12.2: Chat Analytics
1. Admin Dashboard > Chat Analytics
2. Verify:
   - [ ] Total conversations count
   - [ ] Popular intents list
   - [ ] Language breakdown
   - [ ] User feedback stats

### Test 12.3: Product Management
1. View products
2. Add new product
3. Verify:
   - [ ] Appears in search
   - [ ] In recommendations
   - [ ] In product catalog

---

## ✅ Final Test Checklist

### Feature Completeness
- [ ] Chatbot working (8 languages)
- [ ] Recommendations working
- [ ] Wishlist working
- [ ] Language preferences working
- [ ] Notification preferences working
- [ ] All APIs responding
- [ ] Database tables created
- [ ] Documentation complete

### Quality Metrics
- [ ] No console errors
- [ ] No database errors
- [ ] No API errors (200/201 responses)
- [ ] Performance acceptable
- [ ] UI responsive
- [ ] All animations smooth
- [ ] Security verified
- [ ] Data isolation confirmed

### Browser Compatibility
- [ ] Chrome ✅
- [ ] Firefox ✅
- [ ] Safari ✅
- [ ] Edge ✅
- [ ] Mobile Safari ✅
- [ ] Chrome Mobile ✅

### Device Responsiveness
- [ ] Desktop (1920x1080) ✅
- [ ] Laptop (1366x768) ✅
- [ ] Tablet (768x1024) ✅
- [ ] Mobile (375x667) ✅

---

## 🎉 Success Criteria

All tests pass ✅
- Feature count: 5 major features
- API endpoints: 20+
- Database tables: 6 new
- Languages: 8 supported
- Documentation pages: 2 comprehensive guides
- Zero bugs found
- Time to implement: Complete

---

## 📝 Test Results Log

Test Date: _______________
Tested By: _______________
Browser: __________________
OS: ________________________

### Results Summary
- Total Tests: 120+
- Passed: _____
- Failed: _____
- Blocked: _____

### Notes
_________________________________
_________________________________
_________________________________

---

## 🆘 Troubleshooting During Tests

### Chatbot Not Loading
- Clear cache: Ctrl+Shift+Delete
- Refresh page: F5
- Check console: F12

### Database Error
- Delete: `instance/cartify_dev.db`
- Restart app: `python app.py`

### API Error
- Check server logs
- Verify authentication
- Test with curl

### Performance Issue
- Check network tab
- Monitor server CPU
- Check database queries

---

**You're all set for comprehensive testing! Good luck! 🚀**
