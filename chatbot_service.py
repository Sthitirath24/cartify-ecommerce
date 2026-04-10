"""
Multilingual Chatbot Service for Cartify
Supports: English, Hindi, Odia, and other Indian languages
"""

from models import db, MultilingualChatMessage, ChatbotIntentClassification, Product, Order, User
import json
from datetime import datetime
import re

# Multilingual responses dictionary
MULTILINGUAL_RESPONSES = {
    'en': {
        'greeting': 'Hello! Welcome to Cartify. How can I help you today?',
        'search_product': 'I can help you find products. What are you looking for?',
        'not_found': 'Sorry, I couldn\'t find what you\'re looking for. Could you provide more details?',
        'product_available': 'This product is available in stock.',
        'product_unavailable': 'Sorry, this product is currently out of stock.',
        'cart_empty': 'Your cart is empty. Add some products to get started!',
        'order_status': 'Let me check your order status. Please provide your order number.',
        'thanks': 'Thank you for shopping at Cartify! Is there anything else I can help with?',
        'goodbye': 'Goodbye! Have a great day!',
        'error': 'I encountered an error. Please try again or contact support.',
        'general_help': 'I can help with products, orders, shipping, payments, and account support. Ask me anything and I will do my best to help.',
        'shipping_info': 'Shipping options: Standard (5-7 days), Express (2-3 days), Overnight (next day). Shipping charges are shown at checkout.',
        'payment_info': 'We support Cards, UPI, Net Banking, and Cash on Delivery where available.',
        'return_info': 'You can request a return from your orders page. Refunds are processed after item verification.',
        'offer_info': 'You can check current offers on the homepage banners and product pages.',
        'support_info': 'For support, use chat here or contact support@cartify.com.',
        'warranty_info': 'Warranty depends on product type and brand. Check product details for exact warranty terms.',
        'catalog_overview': 'We have products across multiple categories like Electronics, Clothing, Home & Garden, Beauty & Health, Sports & Outdoors, Books & Media, Toys & Games, and Automotive. Tell me a category or product name and I will suggest items.',
    },
    'hi': {
        'greeting': 'नमस्ते! Cartify में आपका स्वागत है। मैं आपकी कैसे मदद कर सकता हूँ?',
        'search_product': 'मैं आपको उत्पाद खोजने में मदद कर सकता हूँ। आप क्या ढूंढ रहे हैं?',
        'not_found': 'खेद है, मुझे आपको ढूंढ नहीं मिला। क्या आप अधिक विवरण प्रदान कर सकते हैं?',
        'product_available': 'यह उत्पाद स्टॉक में उपलब्ध है।',
        'product_unavailable': 'खेद है, यह उत्पाद वर्तमान में स्टॉक से बाहर है।',
        'cart_empty': 'आपकी कार्ट खाली है। शुरू करने के लिए कुछ उत्पाद जोड़ें!',
        'order_status': 'मुझे आपके ऑर्डर की स्थिति की जांच करने दीजिए। कृपया अपना ऑर्डर नंबर प्रदान करें।',
        'thanks': 'Cartify में खरीदारी करने के लिए धन्यवाद! क्या मैं कुछ और आपकी मदद कर सकता हूँ?',
        'goodbye': 'अलविदा! एक बढ़िया दिन हो!',
        'error': 'मुझे एक त्रुटि का सामना करना पड़ा। कृपया पुनः प्रयास करें या समर्थन से संपर्क करें।',
        'general_help': 'मैं उत्पाद, ऑर्डर, शिपिंग, भुगतान और अकाउंट सहायता में मदद कर सकता हूँ। आप कोई भी सवाल पूछ सकते हैं।',
        'shipping_info': 'शिपिंग विकल्प: स्टैंडर्ड (5-7 दिन), एक्सप्रेस (2-3 दिन), ओवरनाइट (अगला दिन)। शुल्क चेकआउट पर दिखेगा।',
        'payment_info': 'हम कार्ड, UPI, नेट बैंकिंग और उपलब्ध होने पर कैश ऑन डिलीवरी स्वीकार करते हैं।',
        'return_info': 'रिटर्न के लिए अपने ऑर्डर पेज से अनुरोध करें। सत्यापन के बाद रिफंड किया जाता है।',
        'offer_info': 'वर्तमान ऑफर होमपेज बैनर और प्रोडक्ट पेज पर देख सकते हैं।',
        'support_info': 'सहायता के लिए यहां चैट करें या support@cartify.com पर संपर्क करें।',
        'warranty_info': 'वारंटी प्रोडक्ट और ब्रांड पर निर्भर करती है। सटीक जानकारी प्रोडक्ट विवरण में देखें।',
        'catalog_overview': 'हमारे पास कई श्रेणियों में उत्पाद हैं जैसे Electronics, Clothing, Home & Garden, Beauty & Health, Sports & Outdoors, Books & Media, Toys & Games और Automotive। आप कोई श्रेणी या प्रोडक्ट नाम बताएं, मैं सुझाव दूंगा।',
    },
    'or': {
        'greeting': 'ନମସ୍କାର! Cartify ରେ ସ୍ୱାଗତଆ। ମୁଁ ଆପଣାଙ୍କୁ କିପରି ସାହାଯ୍ୟ କରିପାରେ?',
        'search_product': 'ମୁଁ ଆପଣାଙ୍କୁ ଉତ୍ପାଦ ଖୋଜିବାରେ ସାହାଯ୍ୟ କରିପାରେ। ଆପଣ କ\'ଣ ଖୋଜୁଛନ୍ତି?',
        'not_found': 'ଅଳସମି, ମୁଁ ଆପଣଙ୍କ ଖୋଜିବା ଅନୁଯାୟୀ ଅସୁଧ ଖୋଜିପାରିଲି। ଆପଣ ଆଉ ଅଧିକ ବିବରଣ ପ୍ରଦାନ କରିପାରିବେନ?',
        'product_available': 'ଏହି ଉତ୍ପାଦ ଷ୍ଟକରେ ଉପଲବ୍ଧ।',
        'product_unavailable': 'ଅଳସମି, ଏହି ଉତ୍ପାଦ ବର୍ତ୍ତମାନ ଷ୍ଟକ ବାହାରେ ଅଛି।',
        'cart_empty': 'ଆପଣଙ୍କ କାର୍ଟ ଖାଲି ଅଛି। ଆରମ୍ଭ କରିବାକୁ ଧାଡ଼ିଆ ଉତ୍ପାଦ ଯୋଡ଼ନ୍ତୁ!',
        'order_status': 'ମୁଁ ଆପଣଙ୍କ ଅର୍ଡର ସ୍ଥିତି ଯାଞ୍ଚ କରିବାକୁ ଦିନ୍ତୋ। ଦୟା କରି ଆପଣଙ୍କ ଅର୍ଡର ସଂଖ୍ୟା ପ୍ରଦାନ କରନ୍ତୁ।',
        'thanks': 'Cartify ରେ କିଣିବା ବାବଦକୁ ଧନ୍ୟବାଦ! ମୁଁ ଆପଣାଙ୍କୁ ଆଉ କିଛି ସାହାଯ୍ୟ କରିପାରେ?',
        'goodbye': 'ବିଦା ନିନ୍ତୁ! ଏକ ଭଲ ଦିନ ଦେବେ!',
        'error': 'ମୁଁ ଏକ ତ୍ରୁଟି ସମ୍ମୁଖୀନ ହେଲି। ଦୟା କରି ପୁନର୍ବାର ଚେଷ୍ଟା କରନ୍ତୁ ବା ସମର୍ଥନ ସହ ଯୋଗାଯୋଗ କରନ୍ତୁ।',
        'general_help': 'ମୁଁ ପଣ୍ୟ, ଅର୍ଡର, ଶିପିଂ, ପେମେଣ୍ଟ ଏବଂ ଅକାଉଣ୍ଟ ସହାୟତାରେ ସହଯୋଗ କରିପାରିବି। ଆପଣ ଯେକୌଣସି ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ।',
        'shipping_info': 'ଶିପିଂ ବିକଳ୍ପ: ସ୍ଟାଣ୍ଡାର୍ଡ, ଏକ୍ସପ୍ରେସ, ଓଭରନାଇଟ। ଚେକଆଉଟରେ ଶୁଳ୍କ ଦେଖାଯିବ।',
        'payment_info': 'କାର୍ଡ, UPI, ନେଟ ବ୍ୟାଙ୍କିଂ ଏବଂ ଉପଲବ୍ଧ ଥିଲେ COD ଗ୍ରହଣ କରାଯାଏ।',
        'return_info': 'ରିଟର୍ନ ପାଇଁ ଅର୍ଡର ପେଜରୁ ଅନୁରୋଧ କରନ୍ତୁ। ଯାଞ୍ଚ ପରେ ରିଫଣ୍ଡ ହେବ।',
        'offer_info': 'ବର୍ତ୍ତମାନର ଅଫର ହୋମପେଜ ଏବଂ ପ୍ରୋଡକ୍ଟ ପେଜରେ ଦେଖିପାରିବେ।',
        'support_info': 'ସହାୟତା ପାଇଁ ଏଠାରେ ଚ୍ୟାଟ କରନ୍ତୁ କିମ୍ବା support@cartify.com ସହ ସଂଯୋଗ କରନ୍ତୁ।',
        'warranty_info': 'ୱାରେଣ୍ଟି ପ୍ରୋଡକ୍ଟ ଓ ବ୍ରାଣ୍ଡ ଉପରେ ନିର୍ଭର କରେ। ପ୍ରୋଡକ୍ଟ ବିବରଣୀ ଦେଖନ୍ତୁ।',
        'catalog_overview': 'ଆମ ପାଖରେ ଅନେକ ବର୍ଗରେ ପଣ୍ୟ ଅଛି, ଯେପରିକି Electronics, Clothing, Home & Garden, Beauty & Health, Sports & Outdoors, Books & Media, Toys & Games ଏବଂ Automotive। ଆପଣ ବର୍ଗ କିମ୍ବା ପଣ୍ୟ ନାମ କହନ୍ତୁ, ମୁଁ ସହାୟତା କରିବି।',
    },
    'ta': {
        'greeting': 'வணக்கம்! Cartify-க்கு வரவேற்கிறோம். நான் உங்களுக்கு எவ்வாறு உதவலாம்?',
        'search_product': 'பொருட்களைக் கண்டறிய நான் உங்களுக்கு உதவலாம். நீங்கள் என்ன தேடுகிறீர்கள்?',
        'not_found': 'மன்னிக்கவும், நான் நீங்கள் தேடுவதைக் கண்டறிய முடியவில்லை। நீங்கள் மேலும் விவரங்களை வழங்க முடியுமா?',
        'product_available': 'இந்த பொருள் இருப்பிலுள்ளது.',
        'product_unavailable': 'மன்னிக்கவும், இந்த பொருள் தற்போது இருப்பு இல்லை.',
        'cart_empty': 'உங்கள் கார்ட் வெறுமையாக உள்ளது. தொடங்க சில பொருட்களைச் சேர்க்கவும்!',
        'order_status': 'உங்கள் ஆர்டர் நிலை சரிபார்க்க அனுமதிக்கவும். தயவாக உங்கள் ஆர்டர் எண்ணை வழங்கவும்.',
        'thanks': 'Cartify-ல் வாங்குவதற்கு நன்றி! நான் வேறு எதையும் உங்களுக்கு உதவ முடியுமா?',
        'goodbye': 'விடைபோக! நல்ல நாள் வேண்டுகிறோம்!',
        'error': 'ஒரு பிழை எனக்கு ஏற்பட்டது. தயவாக மீண்டும் முயற்சிக்கவும் அல்லது ஆதரவை தொடர்பு கொள்ளவும்।',
        'general_help': 'பொருட்கள், ஆர்டர்கள், டெலிவரி, கட்டணம், கணக்கு உதவி போன்றவற்றில் நான் உதவ முடியும். எந்த கேள்வியும் கேளுங்கள்.',
        'shipping_info': 'டெலிவரி விருப்பங்கள்: ஸ்டாண்டர்ட், எக்ஸ்பிரஸ், ஓவர்நைட். கட்டணங்கள் checkout-ல் காட்டப்படும்.',
        'payment_info': 'Cards, UPI, Net Banking, மற்றும் கிடைத்தால் COD ஆகியவை ஆதரிக்கப்படுகின்றன.',
        'return_info': 'Returns-ஐ orders page-ல் இருந்து கோரலாம். சரிபார்ப்புக்குப் பிறகு refund செய்யப்படும்.',
        'offer_info': 'தற்போதைய offers-ஐ homepage banner மற்றும் product pages-ல் பார்க்கலாம்.',
        'support_info': 'உதவிக்கு இங்கே chat செய்யலாம் அல்லது support@cartify.com தொடர்புகொள்ளலாம்.',
        'warranty_info': 'Warranty பொருள் மற்றும் brand அடிப்படையில் மாறும். Product details-ஐ பார்க்கவும்.',
        'catalog_overview': 'எங்களிடம் Electronics, Clothing, Home & Garden, Beauty & Health, Sports & Outdoors, Books & Media, Toys & Games, Automotive போன்ற பல பிரிவுகளில் பொருட்கள் உள்ளன. ஒரு category அல்லது product name சொல்லுங்கள், நான் பரிந்துரைக்கிறேன்.',
    },
    'te': {
        'greeting': 'నమస్కారం! Cartify కి స్వాగతం. నేను మీకు ఎలా సహాయం చేయగలను?',
        'search_product': 'ఉత్పత్తులు కనుగొనడంలో నేను సహాయం చేస్తాను. మీరు ఏమి చూస్తున్నారు?',
        'not_found': 'క్షమించండి, మీరు అడిగింది కనుగొనలేకపోయాను. మరింత వివరాలు ఇవ్వగలరా?',
        'product_available': 'ఈ ఉత్పత్తి స్టాక్‌లో ఉంది.',
        'product_unavailable': 'క్షమించండి, ఈ ఉత్పత్తి ప్రస్తుతం స్టాక్‌లో లేదు.',
        'cart_empty': 'మీ కార్ట్ ఖాళీగా ఉంది. ప్రారంభించడానికి కొన్ని ఉత్పత్తులు జోడించండి!',
        'order_status': 'మీ ఆర్డర్ స్థితి చెక్ చేస్తాను. దయచేసి మీ ఆర్డర్ నంబర్ ఇవ్వండి.',
        'thanks': 'Cartify లో షాపింగ్ చేసినందుకు ధన్యవాదాలు! ఇంకేమైనా సహాయం కావాలా?',
        'goodbye': 'ధన్యవాదాలు! మీ రోజు బాగుండాలి!',
        'error': 'ఒక లోపం జరిగింది. దయచేసి మళ్లీ ప్రయత్నించండి లేదా సపోర్ట్‌ను సంప్రదించండి.',
        'general_help': 'నేను ఉత్పత్తులు, ఆర్డర్లు, షిప్పింగ్, చెల్లింపులు మరియు అకౌంట్ సహాయంలో సహాయం చేయగలను. ఏ ప్రశ్నైనా అడగండి.',
        'shipping_info': 'షిప్పింగ్ ఎంపికలు: స్టాండర్డ్, ఎక్స్‌ప్రెస్, ఓవర్‌నైట్. ఛార్జీలు checkoutలో చూపబడతాయి.',
        'payment_info': 'కార్డులు, UPI, నెట్ బ్యాంకింగ్, మరియు అందుబాటులో ఉంటే COD అందుబాటులో ఉన్నాయి.',
        'return_info': 'రిటర్న్ కోసం మీ orders పేజీ నుంచి రిక్వెస్ట్ చేయండి. ధృవీకరణ తర్వాత రిఫండ్ అవుతుంది.',
        'offer_info': 'ప్రస్తుత ఆఫర్లు homepage banner మరియు product pagesలో చూడవచ్చు.',
        'support_info': 'సహాయం కోసం ఇక్కడ చాట్ చేయండి లేదా support@cartify.com సంప్రదించండి.',
        'warranty_info': 'వారంటీ ఉత్పత్తి మరియు బ్రాండ్‌పై ఆధారపడి ఉంటుంది. వివరాల కోసం product page చూడండి.',
        'catalog_overview': 'మా వద్ద Electronics, Clothing, Home & Garden, Beauty & Health, Sports & Outdoors, Books & Media, Toys & Games, Automotive వంటి విభాగాల్లో ఉత్పత్తులు ఉన్నాయి. మీరు category లేదా product name చెప్పండి, నేను సూచనలు ఇస్తాను.',
    },
    'bn': {
        'greeting': 'নমস্কার! Cartify-তে স্বাগতম। আমি কীভাবে সাহায্য করতে পারি?',
        'search_product': 'আমি আপনাকে পণ্য খুঁজে পেতে সাহায্য করতে পারি। আপনি কী খুঁজছেন?',
        'not_found': 'দুঃখিত, আপনি যা খুঁজছেন তা পাইনি। আরও বিস্তারিত দিতে পারবেন?',
        'product_available': 'এই পণ্যটি স্টকে আছে।',
        'product_unavailable': 'দুঃখিত, এই পণ্যটি এখন স্টকে নেই।',
        'cart_empty': 'আপনার কার্ট খালি। শুরু করতে কিছু পণ্য যোগ করুন!',
        'order_status': 'আমি আপনার অর্ডারের অবস্থা দেখে দিচ্ছি। অনুগ্রহ করে অর্ডার নম্বর দিন।',
        'thanks': 'Cartify-তে কেনাকাটার জন্য ধন্যবাদ! আর কোনো সাহায্য লাগবে?',
        'goodbye': 'বিদায়! আপনার দিনটি শুভ হোক!',
        'error': 'একটি ত্রুটি হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন বা সাপোর্টে যোগাযোগ করুন।',
        'general_help': 'আমি পণ্য, অর্ডার, শিপিং, পেমেন্ট এবং অ্যাকাউন্ট সহায়তায় সাহায্য করতে পারি। যে কোনো প্রশ্ন করতে পারেন।',
        'shipping_info': 'শিপিং অপশন: স্ট্যান্ডার্ড, এক্সপ্রেস, ওভারনাইট। চার্জ checkout-এ দেখা যাবে।',
        'payment_info': 'কার্ড, UPI, নেট ব্যাংকিং এবং যেখানে সম্ভব COD সমর্থিত।',
        'return_info': 'রিটার্নের জন্য orders page থেকে অনুরোধ করুন। যাচাইয়ের পর রিফান্ড হবে।',
        'offer_info': 'চলতি অফার homepage banner এবং product page-এ পাওয়া যাবে।',
        'support_info': 'সহায়তার জন্য এখানে চ্যাট করুন বা support@cartify.com-এ যোগাযোগ করুন।',
        'warranty_info': 'ওয়ারেন্টি পণ্য ও ব্র্যান্ড অনুযায়ী ভিন্ন হয়। বিস্তারিত product page-এ দেখুন।',
        'catalog_overview': 'আমাদের কাছে Electronics, Clothing, Home & Garden, Beauty & Health, Sports & Outdoors, Books & Media, Toys & Games, Automotive সহ বিভিন্ন ক্যাটেগরির পণ্য আছে। ক্যাটেগরি বা পণ্যের নাম বলুন, আমি সাজেস্ট করব।',
    },
    'mr': {
        'greeting': 'नमस्कार! Cartify मध्ये आपले स्वागत आहे. मी तुमची कशी मदत करू?',
        'search_product': 'मी तुम्हाला उत्पादने शोधण्यात मदत करू शकतो. तुम्ही काय शोधत आहात?',
        'not_found': 'क्षमस्व, तुम्ही शोधत असलेली गोष्ट सापडली नाही. अधिक तपशील द्याल का?',
        'product_available': 'हे उत्पादन स्टॉकमध्ये उपलब्ध आहे.',
        'product_unavailable': 'क्षमस्व, हे उत्पादन सध्या स्टॉकमध्ये नाही.',
        'cart_empty': 'तुमची कार्ट रिकामी आहे. सुरुवात करण्यासाठी काही उत्पादने जोडा!',
        'order_status': 'मी तुमच्या ऑर्डरची स्थिती तपासतो. कृपया ऑर्डर नंबर द्या.',
        'thanks': 'Cartify मध्ये खरेदी केल्याबद्दल धन्यवाद! आणखी काही मदत हवी आहे का?',
        'goodbye': 'नमस्कार! तुमचा दिवस छान जावो!',
        'error': 'त्रुटी आली. कृपया पुन्हा प्रयत्न करा किंवा सपोर्टशी संपर्क करा.',
        'general_help': 'मी उत्पादने, ऑर्डर, शिपिंग, पेमेंट आणि अकाउंट सहाय्यामध्ये मदत करू शकतो. कोणताही प्रश्न विचारा.',
        'shipping_info': 'शिपिंग पर्याय: स्टँडर्ड, एक्सप्रेस, ओव्हरनाईट. शुल्क checkout मध्ये दिसेल.',
        'payment_info': 'कार्ड, UPI, नेट बँकिंग आणि उपलब्ध असल्यास COD स्वीकारले जाते.',
        'return_info': 'रिटर्नसाठी orders पेजवरून विनंती करा. पडताळणीनंतर रिफंड केला जाईल.',
        'offer_info': 'सध्याचे ऑफर्स homepage banner आणि product pages वर पहा.',
        'support_info': 'मदतीसाठी इथे चॅट करा किंवा support@cartify.com वर संपर्क करा.',
        'warranty_info': 'वॉरंटी उत्पादन आणि ब्रँडनुसार बदलते. तपशीलासाठी product page पहा.',
        'catalog_overview': 'आमच्याकडे Electronics, Clothing, Home & Garden, Beauty & Health, Sports & Outdoors, Books & Media, Toys & Games, Automotive अशा अनेक श्रेणींमध्ये उत्पादने आहेत. तुम्ही category किंवा product name सांगा, मी सुचवतो.',
    },
    'gu': {
        'greeting': 'નમસ્તે! Cartify માં આપનું સ્વાગત છે. હું કેવી રીતે મદદ કરી શકું?',
        'search_product': 'હું તમને પ્રોડક્ટ શોધવામાં મદદ કરી શકું છું. તમે શું શોધી રહ્યા છો?',
        'not_found': 'માફ કરશો, તમે જે શોધી રહ્યા છો તે મળ્યું નથી. વધુ વિગતો આપશો?',
        'product_available': 'આ પ્રોડક્ટ સ્ટોકમાં ઉપલબ્ધ છે.',
        'product_unavailable': 'માફ કરશો, આ પ્રોડક્ટ હાલમાં સ્ટોકમાં નથી.',
        'cart_empty': 'તમારું કાર્ટ ખાલી છે. શરૂઆત કરવા માટે થોડા પ્રોડક્ટ ઉમેરો!',
        'order_status': 'હું તમારા ઓર્ડરની સ્થિતિ તપાસું છું. કૃપા કરીને ઓર્ડર નંબર આપો.',
        'thanks': 'Cartify પર ખરીદી કરવા બદલ આભાર! શું હું વધુ મદદ કરી શકું?',
        'goodbye': 'આવજો! તમારો દિવસ સારો જાય!',
        'error': 'એક ભૂલ થઈ. કૃપા કરીને ફરી પ્રયાસ કરો અથવા સપોર્ટનો સંપર્ક કરો.',
        'general_help': 'હું પ્રોડક્ટ્સ, ઓર્ડર, શિપિંગ, ચુકવણી અને એકાઉન્ટ સહાયમાં મદદ કરી શકું છું. તમે કોઈપણ પ્રશ્ન પૂછો.',
        'shipping_info': 'શિપિંગ વિકલ્પો: સ્ટાન્ડર્ડ, એક્સપ્રેસ, ઓવરનાઇટ. ચાર્જીસ checkout દરમિયાન દેખાશે.',
        'payment_info': 'કાર્ડ, UPI, નેટ બેન્કિંગ અને ઉપલબ્ધ હોય તો COD સપોર્ટેડ છે.',
        'return_info': 'રિટર્ન માટે orders પેજમાંથી વિનંતી કરો. ચકાસણી પછી રિફંડ થશે.',
        'offer_info': 'હાલના offers homepage banner અને product pages પર જોઈ શકો છો.',
        'support_info': 'મદદ માટે અહીં ચેટ કરો અથવા support@cartify.com પર સંપર્ક કરો.',
        'warranty_info': 'વોરંટી પ્રોડક્ટ અને બ્રાન્ડ પર આધારિત છે. વિગતો માટે product page જુઓ.',
        'catalog_overview': 'અમારી પાસે Electronics, Clothing, Home & Garden, Beauty & Health, Sports & Outdoors, Books & Media, Toys & Games અને Automotive જેવી કેટેગરીમાં પ્રોડક્ટ્સ છે. તમે category અથવા product નામ કહો, હું સૂચન કરું.',
    },
}

# Intent keywords for different languages
INTENT_KEYWORDS = {
    'product_search': {
        'en': ['find', 'search', 'looking for', 'show', 'buy', 'product'],
        'hi': ['खोज', 'खोजें', 'ढूंढ', 'चाहिए', 'दिखाओ', 'चाहता', 'देना'],
        'or': ['ଖୋଜନ୍ତୁ', 'ଖୋଜନ୍ତୁ', 'ଦିଖାନ୍ତୁ', 'ବିଚାର', 'ଚାହିଁ'],
        'ta': ['தேடு', 'கண்டறி', 'விரும்பு', 'வேண்டும்', 'கொடு', 'காட்டு'],
    },
    'order_status': {
        'en': ['order', 'status', 'where', 'tracking', 'delivery', 'when', 'arrived'],
        'hi': ['ऑर्डर', 'स्थिति', 'कहाँ', 'ट्रैकिंग', 'डिलीवरी', 'कब', 'आया'],
        'or': ['ଅର୍ଡର', 'ସ୍ଥିତି', 'ସତେେ�େେଁ', 'ଟ୍ର୍ୟାକିଙ୍ଗ', 'ଡିଲିଭରି', 'କେତେ'],
        'ta': ['ஆர்டர்', 'நிலை', 'எங்கே', 'கண்காணிப்பு', 'டெலিவரி', 'எப்போது'],
    },
    'cart_management': {
        'en': ['cart', 'add', 'remove', 'checkout', 'pay', 'price', 'cost', 'total'],
        'hi': ['कार्ट', 'जोड़ना', 'हटाना', 'चेकआउट', 'भुगतान', 'कीमत'],
        'or': ['କାର୍ଟ', 'ଯୋଡ଼ନ୍ତୁ', 'ହଟାନ୍ତୁ', 'ଚେକଆଉଟ', 'ଭୁଗତାନ', 'ମୂଲ୍ୟ'],
        'ta': ['கார்ட்', 'சேர்', 'அகற்று', 'சரிபார்ப்பு', 'பணம்', 'விலை'],
    },
    'account': {
        'en': ['account', 'profile', 'login', 'password', 'email', 'phone', 'address'],
        'hi': ['खाता', 'प्रोफाइल', 'लॉगिन', 'पासवर्ड', 'ईमेल', 'फोन'],
        'or': ['ଖାତା', 'ପ୍ରୋଫାଇଲ', 'ଲଗଇନ', 'ପାସୱର୍ଡ', 'ଇମେଲ', 'ଫୋନ'],
        'ta': ['கணக்கு', 'சுயவிவரம்', 'உள்நுழைய', 'கடவுசொல்', 'ईмेल', 'தொலைபேசி'],
    },
}

FAQ_INTENTS = {
    'shipping_info': ['shipping', 'delivery', 'ship', 'डिलीवरी', 'शिपिंग', 'ଡିଲିଭରି', 'டெலிவரி', 'షిప్పింగ్', 'ডেলিভারি', 'शिपिंग', 'ડિલિવરી'],
    'payment_info': ['payment', 'pay', 'upi', 'card', 'cod', 'भुगतान', 'पेमेंट', 'ପେମେଣ୍ଟ', 'கட்டணம்', 'చెల్లింపు', 'পেমেন্ট', 'पेमेंट', 'ચુકવણી'],
    'return_info': ['return', 'refund', 'exchange', 'replace', 'रिटर्न', 'रिफंड', 'ରିଟର୍ନ', 'रिफंड', 'ரிட்டர்ன்', 'రిటర్న్', 'রিটার্ন', 'रिटर्न', 'રિટર્ન'],
    'offer_info': ['offer', 'discount', 'deal', 'coupon', 'ऑफर', 'छूट', 'ଅଫର', 'தள்ளுபடி', 'ఆఫర్', 'অফার', 'ऑफर', 'ઓફર'],
    'support_info': ['help', 'support', 'contact', 'assist', 'मदद', 'सहायता', 'ସହାୟତା', 'உதவி', 'సహాయం', 'সহায়তা', 'मदत', 'મદદ'],
    'warranty_info': ['warranty', 'guarantee', 'वारंटी', 'ଗ୍ୟାରାଣ୍ଟି', 'உத்தரவாதம்', 'వారంటీ', 'ওয়ারেন্টি', 'वॉरंटी', 'વોરંટી']
}

CATALOG_QUERY_KEYWORDS = [
    'what products', 'products do you have', 'what do you have', 'show products', 'all products',
    'कौन से उत्पाद', 'आपके पास क्या', 'ପଣ୍ୟ ଅଛି', 'என்ன பொருட்கள்', 'ఏ ఉత్పత్తులు',
    'কি পণ্য', 'कोणती उत्पादने', 'કયા પ્રોડક્ટ્સ'
]


class MultilingualChatbot:
    """Handles multilingual chatbot responses and intent classification"""
    
    def __init__(self):
        self.responses = MULTILINGUAL_RESPONSES
        self.intent_keywords = INTENT_KEYWORDS
    
    def detect_language(self, text):
        """Detect language from text"""
        # Simple heuristic: check if text contains language-specific characters
        if any('\u0900' <= char <= '\u097F' for char in text):  # Devanagari (Hindi)
            return 'hi'
        elif any('\u0B00' <= char <= '\u0B7F' for char in text):  # Odia
            return 'or'
        elif any('\u0B80' <= char <= '\u0BFF' for char in text):  # Tamil
            return 'ta'
        return 'en'  # Default to English
    
    def classify_intent(self, text, language='en'):
        """Classify the intent of user message"""
        text_lower = text.lower()
        max_score = 0
        detected_intent = 'general'
        
        for intent, keywords in self.intent_keywords.items():
            lang_keywords = keywords.get(language, keywords.get('en', []))
            score = sum(1 for keyword in lang_keywords if keyword.lower() in text_lower)
            
            if score > max_score:
                max_score = score
                detected_intent = intent
        
        confidence = min(max_score / 3, 1.0)  # Normalize confidence
        return detected_intent, confidence

    def _matches_keywords(self, text, keywords):
        text_lower = text.lower()
        tokens = set(re.findall(r'\w+', text_lower))
        for keyword in keywords:
            key = keyword.lower().strip()
            if not key:
                continue
            # For short single-word triggers like "hi", require exact token match.
            if len(key) <= 3 and ' ' not in key:
                if key in tokens:
                    return True
            else:
                if key in text_lower:
                    return True
        return False

    def detect_faq_intent(self, text):
        text_lower = text.lower()
        for intent_key, keywords in FAQ_INTENTS.items():
            if any(keyword.lower() in text_lower for keyword in keywords):
                return intent_key
        return None

    def is_catalog_query(self, text):
        return self._matches_keywords(text, CATALOG_QUERY_KEYWORDS)

    def get_catalog_overview(self, language='en'):
        try:
            categories = db.session.query(Product.category).distinct().all()
            category_names = [c[0] for c in categories if c and c[0]]
            total_products = Product.query.filter_by(is_active=True).count()

            if category_names:
                category_text = ', '.join(sorted(category_names))
                return f"{self.get_response('catalog_overview', language)}\n\nTotal active products: {total_products}\nCategories: {category_text}"
        except Exception:
            pass
        return self.get_response('catalog_overview', language)
    
    def extract_product_query(self, text):
        """Extract product search query from text"""
        # Remove common words and extract query
        common_words = {'find', 'search', 'show', 'get', 'want', 'looking', 'for', 'me', 'please', 'एक', 'मुझे', 'कृपया'}
        words = text.lower().split()
        query = ' '.join([w for w in words if w not in common_words])
        return query.strip() if query else None
    
    def search_products(self, query, limit=5):
        """Search products by name or category"""
        if not query:
            return [], 0.0
        
        try:
            # Search by product name or category
            products = Product.query.filter(
                (Product.name.ilike(f'%{query}%')) |
                (Product.category.ilike(f'%{query}%')) |
                (Product.description.ilike(f'%{query}%'))
            ).filter_by(is_active=True).limit(limit).all()
            
            if products:
                confidence = 0.9 if query.lower() in [p.name.lower() for p in products] else 0.7
            else:
                confidence = 0.3
            
            return products, confidence
        except Exception as e:
            print(f"Product search error: {e}")
            return [], 0.0
    
    def get_product_response(self, products, language='en'):
        """Generate response with product information"""
        if not products:
            return self.get_response('not_found', language)
        
        response = ""
        for i, product in enumerate(products, 1):
            response += f"\n{i}. {product.name} - ₹{product.price}\n"
            response += f"   {product.category}\n"
            if product.stock_quantity > 0:
                response += f"   ✓ {self.get_response('product_available', language)}\n"
            else:
                response += f"   ✗ {self.get_response('product_unavailable', language)}\n"
        
        return response
    
    def get_order_status(self, user_id, order_number=None):
        """Get order status for user"""
        try:
            if order_number:
                order = Order.query.filter_by(order_number=order_number, user_id=user_id).first()
            else:
                order = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).first()
            
            if order:
                return order, 0.95
            return None, 0.3
        except Exception as e:
            print(f"Order status error: {e}")
            return None, 0.0
    
    def generate_response(self, user_message, language='en', user_id=None, intent=None):
        """Generate chatbot response based on intent"""
        try:
            # Handle common conversational messages first
            greetings = ['hello', 'hi', 'hey', 'namaste', 'namaskar', 'నమస్కారం', 'வணக்கம்', 'নমস্কার', 'નમસ્તે', 'नमस्कार', 'ନମସ୍କାର']
            thanks_words = ['thanks', 'thank you', 'dhanyavad', 'धन्यवाद', 'ଧନ୍ୟବାଦ', 'நன்றி', 'ధన్యవాదాలు', 'ধন্যবাদ', 'आभार', 'આભાર']
            bye_words = ['bye', 'goodbye', 'see you', 'विदा', 'अलविदा', 'ବିଦାୟ', 'பை', 'వీడ్కోలు', 'বিদায়', 'નમસ્તે']

            if self._matches_keywords(user_message, greetings):
                return self.get_response('greeting', language), 'general', 0.9
            if self._matches_keywords(user_message, thanks_words):
                return self.get_response('thanks', language), 'general', 0.9
            if self._matches_keywords(user_message, bye_words):
                return self.get_response('goodbye', language), 'general', 0.9

            if self.is_catalog_query(user_message):
                return self.get_catalog_overview(language), 'catalog_overview', 0.95

            faq_intent = self.detect_faq_intent(user_message)
            if faq_intent:
                return self.get_response(faq_intent, language), faq_intent, 0.9

            if not intent:
                intent, confidence = self.classify_intent(user_message, language)
            else:
                confidence = 0.8
            
            response = ""
            
            if intent == 'product_search':
                query = self.extract_product_query(user_message)
                if not query:
                    response = self.get_response('search_product', language)
                    confidence = 0.6
                else:
                    products, conf = self.search_products(query)
                    response = self.get_product_response(products, language)
                    confidence = conf
            
            elif intent == 'order_status' and user_id:
                # Extract order number if present
                order_number_match = re.search(r'ORD-\d+', user_message)
                order_number = order_number_match.group(0) if order_number_match else None
                
                order, conf = self.get_order_status(user_id, order_number)
                if order:
                    response = f"Order {order.order_number}:\n"
                    response += f"Status: {order.order_status}\n"
                    response += f"Total: ₹{int(order.total_amount)}\n"
                    response += f"Items: {len(order.order_items)}\n"
                    confidence = conf
                else:
                    response = self.get_response('order_status', language)
            
            else:
                # Avoid repetitive "not found" for generic questions.
                response = self.get_response('general_help', language)
                confidence = max(confidence, 0.5)
            
            return response, intent, confidence
        
        except Exception as e:
            print(f"Response generation error: {e}")
            return self.get_response('error', language), 'general', 0.0
    
    def get_response(self, key, language='en'):
        """Get multilingual response"""
        if language not in self.responses:
            language = 'en'
        return self.responses[language].get(key, self.responses['en'].get(key, ''))
    
    def log_chat_message(self, user_id, session_id, language, user_message, bot_response, intent, confidence):
        """Log chat message to database"""
        try:
            chat_msg = MultilingualChatMessage(
                user_id=user_id,
                session_id=session_id,
                language_code=language,
                user_message=user_message,
                bot_response=bot_response,
                intent=intent,
                confidence=confidence
            )
            db.session.add(chat_msg)
            db.session.commit()
            return chat_msg.to_dict()
        except Exception as e:
            print(f"Chat logging error: {e}")
            return None


# Create a global chatbot instance
chatbot = MultilingualChatbot()
