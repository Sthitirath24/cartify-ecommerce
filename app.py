from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import json
import os
import re
from datetime import datetime, timedelta
import random
import uuid

from config import config
from models import (
    db, User, Product, Order, OrderItem, CartItem, Review, ChatMessage, 
    LoyaltyPoints, LoyaltyTransaction, Wishlist, ProductRecommendation,
    UserLanguagePreference, MultilingualChatMessage, NotificationPreference,
    ChatbotIntentClassification
)
from auth import login_required, admin_required, get_current_user, login_user, logout_user
from email_service import init_mail, send_email_verification, send_password_reset_email, send_welcome_email
from api_routes import api_bp
from enhanced_chatbot import enhanced_chatbot
from recommendation_service import recommendation_engine

app = Flask(__name__)

# Configuration
# Use environment variable or default to SQLite development for now
config_name = os.environ.get('FLASK_ENV') or 'development'
if config_name not in config:
    config_name = 'development'  # Fallback to SQLite if config not available
app.config.from_object(config[config_name])
config[config_name].init_app(app)

# Initialize extensions
db.init_app(app)
init_mail(app)

# Register new API blueprint
app.register_blueprint(api_bp)

def get_local_products():
    products = [
        {
            'id': 1,
            'name': 'iPhone 15 Pro Max',
            'price': 149999.0,
            'category': 'Electronics',
            'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400',
            'description': 'Latest iPhone with A17 Pro chip, titanium design, and advanced camera system.',
            'rating': 4.8,
            'reviews': 1247,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 2,
            'name': 'Samsung Galaxy S24 Ultra',
            'price': 129999.0,
            'category': 'Electronics',
            'image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400',
            'description': 'Premium Android flagship with S Pen, 200MP camera, and AI features.',
            'rating': 4.7,
            'reviews': 892,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 3,
            'name': 'MacBook Air M3',
            'price': 114999.0,
            'category': 'Electronics',
            'image': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400',
            'description': 'Ultra-thin laptop with Apple M3 chip, 18-hour battery life.',
            'rating': 4.9,
            'reviews': 567,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 4,
            'name': 'Sony WH-1000XM5 Headphones',
            'price': 29999.0,
            'category': 'Electronics',
            'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
            'description': 'Industry-leading noise cancellation with exceptional sound quality.',
            'rating': 4.8,
            'reviews': 2341,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 5,
            'name': 'iPad Pro 12.9-inch',
            'price': 89999.0,
            'category': 'Electronics',
            'image': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400',
            'description': 'Most powerful iPad with M2 chip and Liquid Retina XDR display.',
            'rating': 4.7,
            'reviews': 445,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 6,
            'name': 'Premium Cotton T-Shirt',
            'price': 1299.0,
            'category': 'Clothing',
            'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
            'description': '100% organic cotton t-shirt with comfortable fit and stylish design.',
            'rating': 4.5,
            'reviews': 1234,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 7,
            'name': 'Denim Jacket Classic',
            'price': 3499.0,
            'category': 'Clothing',
            'image': 'https://images.unsplash.com/photo-1544022613-e87ca540b5c5?w=400',
            'description': 'Timeless denim jacket perfect for any casual occasion.',
            'rating': 4.6,
            'reviews': 789,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 8,
            'name': 'Formal Business Suit',
            'price': 8999.0,
            'category': 'Clothing',
            'image': 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400',
            'description': 'Professional business suit with premium wool blend fabric.',
            'rating': 4.7,
            'reviews': 456,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 9,
            'name': 'Running Shoes Pro',
            'price': 2499.0,
            'category': 'Clothing',
            'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
            'description': 'High-performance running shoes with advanced cushioning technology.',
            'rating': 4.8,
            'reviews': 1678,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 10,
            'name': 'Winter Coat Premium',
            'price': 5999.0,
            'category': 'Clothing',
            'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
            'description': 'Warm winter coat with down insulation and water-resistant exterior.',
            'rating': 4.6,
            'reviews': 567,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 11,
            'name': 'Smart LED Bulb Set',
            'price': 1999.0,
            'category': 'Home & Garden',
            'image': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400',
            'description': 'WiFi-enabled smart bulbs with voice control and customizable colors.',
            'rating': 4.4,
            'reviews': 892,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 12,
            'name': 'Kitchen Mixer Professional',
            'price': 8999.0,
            'category': 'Home & Garden',
            'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400',
            'description': 'Professional-grade stand mixer for all your baking needs.',
            'rating': 4.8,
            'reviews': 1234,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 13,
            'name': 'Garden Tool Set',
            'price': 3499.0,
            'category': 'Home & Garden',
            'image': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400',
            'description': 'Complete garden tool set with ergonomic handles and durable construction.',
            'rating': 4.5,
            'reviews': 678,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 14,
            'name': 'Coffee Maker Deluxe',
            'price': 5499.0,
            'category': 'Home & Garden',
            'image': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400',
            'description': 'Programmable coffee maker with built-in grinder and thermal carafe.',
            'rating': 4.7,
            'reviews': 945,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 15,
            'name': 'Bedding Set Premium',
            'price': 3999.0,
            'category': 'Home & Garden',
            'image': 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400',
            'description': 'Luxury bedding set with 1000 thread count Egyptian cotton.',
            'rating': 4.6,
            'reviews': 567,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 16,
            'name': 'Skincare Set Complete',
            'price': 2499.0,
            'category': 'Beauty & Health',
            'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400',
            'description': 'Complete skincare routine with cleanser, toner, serum, and moisturizer.',
            'rating': 4.7,
            'reviews': 1234,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 17,
            'name': 'Hair Dryer Professional',
            'price': 3999.0,
            'category': 'Beauty & Health',
            'image': 'https://images.unsplash.com/photo-1522338140263-f46f5913618a?w=400',
            'description': 'Professional hair dryer with ionic technology and multiple heat settings.',
            'rating': 4.5,
            'reviews': 789,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 18,
            'name': 'Fitness Tracker Smart',
            'price': 2999.0,
            'category': 'Beauty & Health',
            'image': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400',
            'description': 'Advanced fitness tracker with heart rate monitoring and GPS.',
            'rating': 4.6,
            'reviews': 1456,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 19,
            'name': 'Yoga Mat Premium',
            'price': 1499.0,
            'category': 'Beauty & Health',
            'image': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400',
            'description': 'Non-slip yoga mat with extra cushioning for comfort during practice.',
            'rating': 4.4,
            'reviews': 567,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 20,
            'name': 'Perfume Collection',
            'price': 4999.0,
            'category': 'Beauty & Health',
            'image': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400',
            'description': 'Luxury perfume collection with long-lasting fragrances.',
            'rating': 4.8,
            'reviews': 234,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 21,
            'name': 'Mountain Bike Adventure',
            'price': 24999.0,
            'category': 'Sports & Outdoors',
            'image': 'https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=400',
            'description': 'Professional mountain bike with full suspension and disc brakes.',
            'rating': 4.7,
            'reviews': 345,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 22,
            'name': 'Tennis Racket Pro',
            'price': 3999.0,
            'category': 'Sports & Outdoors',
            'image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=400',
            'description': 'Professional tennis racket with advanced string technology.',
            'rating': 4.6,
            'reviews': 234,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 23,
            'name': 'Camping Tent 4-Person',
            'price': 8999.0,
            'category': 'Sports & Outdoors',
            'image': 'https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?w=400',
            'description': 'Spacious 4-person camping tent with weather-resistant material.',
            'rating': 4.5,
            'reviews': 456,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 24,
            'name': 'Fishing Rod Complete',
            'price': 2999.0,
            'category': 'Sports & Outdoors',
            'image': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400',
            'description': 'Complete fishing rod set with reel, line, and tackle box.',
            'rating': 4.4,
            'reviews': 178,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 25,
            'name': 'Gym Equipment Set',
            'price': 15999.0,
            'category': 'Sports & Outdoors',
            'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400',
            'description': 'Complete home gym set with weights, bench, and resistance bands.',
            'rating': 4.8,
            'reviews': 234,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 26,
            'name': 'Best Seller Novel Collection',
            'price': 1499.0,
            'category': 'Books & Media',
            'image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400',
            'description': 'Collection of bestselling novels in hardcover format.',
            'rating': 4.6,
            'reviews': 1234,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 27,
            'name': 'Bluetooth Speaker Portable',
            'price': 1999.0,
            'category': 'Books & Media',
            'image': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400',
            'description': 'Portable Bluetooth speaker with 20-hour battery life and waterproof design.',
            'rating': 4.5,
            'reviews': 892,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 28,
            'name': 'Gaming Console Pro',
            'price': 39999.0,
            'category': 'Books & Media',
            'image': 'https://images.unsplash.com/photo-1486401899868-0e435ed85128?w=400',
            'description': 'Latest gaming console with 4K graphics and included controller.',
            'rating': 4.9,
            'reviews': 567,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 29,
            'name': 'Camera DSLR Professional',
            'price': 59999.0,
            'category': 'Books & Media',
            'image': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400',
            'description': 'Professional DSLR camera with 24MP sensor and 4K video recording.',
            'rating': 4.8,
            'reviews': 234,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 30,
            'name': 'Wireless Earbuds Sport',
            'price': 3999.0,
            'category': 'Books & Media',
            'image': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400',
            'description': 'Sport wireless earbuds with sweat resistance and secure fit.',
            'rating': 4.7,
            'reviews': 1456,
            'in_stock': True,
            'source': 'Local Database'
        },
        # New Products - Electronics
        {
            'id': 31,
            'name': 'Samsung 55" 4K Smart TV',
            'price': 45999.0,
            'category': 'Electronics',
            'image': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400',
            'description': 'Crystal UHD 4K Smart TV with HDR10+ and built-in Alexa.',
            'rating': 4.6,
            'reviews': 892,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 32,
            'name': 'Apple Watch Series 9',
            'price': 41999.0,
            'category': 'Electronics',
            'image': 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400',
            'description': 'Advanced health monitoring with ECG app and always-on Retina display.',
            'rating': 4.8,
            'reviews': 1567,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 33,
            'name': 'Dell XPS 13 Laptop',
            'price': 89999.0,
            'category': 'Electronics',
            'image': 'https://images.unsplash.com/photo-1593642632823-8f78536788c6?w=400',
            'description': 'Ultra-thin laptop with InfinityEdge display and Intel Core i7.',
            'rating': 4.5,
            'reviews': 678,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 34,
            'name': 'Bose SoundLink Speaker',
            'price': 14999.0,
            'category': 'Electronics',
            'image': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400',
            'description': 'Portable Bluetooth speaker with 360-degree sound and 12-hour battery.',
            'rating': 4.7,
            'reviews': 2341,
            'in_stock': True,
            'source': 'Local Database'
        },
        # New Products - Clothing
        {
            'id': 35,
            'name': 'Leather Jacket Premium',
            'price': 7999.0,
            'category': 'Clothing',
            'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400',
            'description': 'Genuine leather jacket with quilted lining and multiple pockets.',
            'rating': 4.6,
            'reviews': 445,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 36,
            'name': 'Summer Dress Floral',
            'price': 2499.0,
            'category': 'Clothing',
            'image': 'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400',
            'description': 'Lightweight floral dress perfect for summer occasions.',
            'rating': 4.5,
            'reviews': 892,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 37,
            'name': 'Sports Tracksuit Set',
            'price': 3499.0,
            'category': 'Clothing',
            'image': 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400',
            'description': 'Comfortable tracksuit for workouts and casual wear.',
            'rating': 4.4,
            'reviews': 567,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 38,
            'name': 'Wool Sweater Classic',
            'price': 1999.0,
            'category': 'Clothing',
            'image': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400',
            'description': 'Soft merino wool sweater available in multiple colors.',
            'rating': 4.7,
            'reviews': 1234,
            'in_stock': True,
            'source': 'Local Database'
        },
        # New Products - Home & Garden
        {
            'id': 39,
            'name': 'Robot Vacuum Cleaner',
            'price': 24999.0,
            'category': 'Home & Garden',
            'image': 'https://images.unsplash.com/photo-1589894404892-7310b9b39dc9?w=400',
            'description': 'Smart robot vacuum with mapping technology and app control.',
            'rating': 4.5,
            'reviews': 3456,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 40,
            'name': 'Air Purifier HEPA',
            'price': 12999.0,
            'category': 'Home & Garden',
            'image': 'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400',
            'description': 'True HEPA filter removes 99.97% of airborne particles.',
            'rating': 4.6,
            'reviews': 1890,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 41,
            'name': 'Indoor Plant Set',
            'price': 1499.0,
            'category': 'Home & Garden',
            'image': 'https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?w=400',
            'description': 'Set of 3 low-maintenance indoor plants with decorative pots.',
            'rating': 4.8,
            'reviews': 2234,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 42,
            'name': 'Non-Stick Cookware Set',
            'price': 4999.0,
            'category': 'Home & Garden',
            'image': 'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=400',
            'description': '10-piece cookware set with granite coating and glass lids.',
            'rating': 4.7,
            'reviews': 1567,
            'in_stock': True,
            'source': 'Local Database'
        },
        # New Products - Beauty & Health
        {
            'id': 43,
            'name': 'Electric Toothbrush Pro',
            'price': 3499.0,
            'category': 'Beauty & Health',
            'image': 'https://images.unsplash.com/photo-1559671088-795c793c5eb5?w=400',
            'description': 'Sonic toothbrush with pressure sensor and 5 cleaning modes.',
            'rating': 4.6,
            'reviews': 3456,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 44,
            'name': 'Massage Gun Deep Tissue',
            'price': 5999.0,
            'category': 'Beauty & Health',
            'image': 'https://images.unsplash.com/photo-1615461066842-32561977e3d8?w=400',
            'description': 'Percussion massager with 6 attachments and 20 speed levels.',
            'rating': 4.7,
            'reviews': 2890,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 45,
            'name': 'Organic Face Cream',
            'price': 899.0,
            'category': 'Beauty & Health',
            'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400',
            'description': 'Natural anti-aging cream with vitamin C and hyaluronic acid.',
            'rating': 4.5,
            'reviews': 4567,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 46,
            'name': 'Digital Body Scale',
            'price': 1999.0,
            'category': 'Beauty & Health',
            'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400',
            'description': 'Smart scale with body composition analysis and app sync.',
            'rating': 4.4,
            'reviews': 1234,
            'in_stock': True,
            'source': 'Local Database'
        },
        # New Products - Sports & Outdoors
        {
            'id': 47,
            'name': 'Treadmill Home Pro',
            'price': 34999.0,
            'category': 'Sports & Outdoors',
            'image': 'https://images.unsplash.com/photo-1578763460782-913dcf520e91?w=400',
            'description': 'Foldable treadmill with incline and heart rate monitoring.',
            'rating': 4.6,
            'reviews': 890,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 48,
            'name': 'Basketball Official Size',
            'price': 1499.0,
            'category': 'Sports & Outdoors',
            'image': 'https://images.unsplash.com/photo-1519861531473-920026393112?w=400',
            'description': 'Professional basketball with superior grip and durability.',
            'rating': 4.8,
            'reviews': 2345,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 49,
            'name': 'Yoga Block Set',
            'price': 799.0,
            'category': 'Sports & Outdoors',
            'image': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400',
            'description': '2 foam yoga blocks with strap for enhanced flexibility.',
            'rating': 4.5,
            'reviews': 1567,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 50,
            'name': 'Swimming Goggles Pro',
            'price': 999.0,
            'category': 'Sports & Outdoors',
            'image': 'https://images.unsplash.com/photo-1560090995-01632a28895b?w=400',
            'description': 'Anti-fog goggles with UV protection and adjustable fit.',
            'rating': 4.6,
            'reviews': 3456,
            'in_stock': True,
            'source': 'Local Database'
        },
        # New Products - Books & Media
        {
            'id': 51,
            'name': 'Kindle Paperwhite',
            'price': 12999.0,
            'category': 'Books & Media',
            'image': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400',
            'description': 'Waterproof e-reader with 6.8" display and adjustable warm light.',
            'rating': 4.9,
            'reviews': 5678,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 52,
            'name': 'Vinyl Record Player',
            'price': 8999.0,
            'category': 'Books & Media',
            'image': 'https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=400',
            'description': 'Retro turntable with Bluetooth and built-in speakers.',
            'rating': 4.7,
            'reviews': 1234,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 53,
            'name': 'Acoustic Guitar Starter',
            'price': 5999.0,
            'category': 'Books & Media',
            'image': 'https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=400',
            'description': 'Full-size acoustic guitar with accessories and learning app.',
            'rating': 4.6,
            'reviews': 2890,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 54,
            'name': 'Drone with 4K Camera',
            'price': 24999.0,
            'category': 'Books & Media',
            'image': 'https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=400',
            'description': 'GPS drone with 4K camera, 30min flight time and follow mode.',
            'rating': 4.5,
            'reviews': 890,
            'in_stock': True,
            'source': 'Local Database'
        },
        # New Category - Toys & Games
        {
            'id': 55,
            'name': 'LEGO Star Wars Set',
            'price': 7999.0,
            'category': 'Toys & Games',
            'image': 'https://images.unsplash.com/photo-1585366119957-e9730b6d0f60?w=400',
            'description': 'Ultimate Collector Series Millennium Falcon with 7541 pieces.',
            'rating': 4.9,
            'reviews': 3456,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 56,
            'name': 'Board Game Collection',
            'price': 2999.0,
            'category': 'Toys & Games',
            'image': 'https://images.unsplash.com/photo-1610890716171-6b1c9f2bd40c?w=400',
            'description': 'Set of 5 classic board games for family game night.',
            'rating': 4.7,
            'reviews': 1234,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 57,
            'name': 'Remote Control Car',
            'price': 3499.0,
            'category': 'Toys & Games',
            'image': 'https://images.unsplash.com/photo-1594787318286-3d835c1d207f?w=400',
            'description': 'High-speed RC car with 4WD and 50m control range.',
            'rating': 4.5,
            'reviews': 2345,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 58,
            'name': 'Puzzle 1000 Pieces',
            'price': 999.0,
            'category': 'Toys & Games',
            'image': 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400',
            'description': 'Beautiful landscape puzzle with premium quality pieces.',
            'rating': 4.6,
            'reviews': 5678,
            'in_stock': True,
            'source': 'Local Database'
        },
        # New Category - Automotive
        {
            'id': 59,
            'name': 'Car Vacuum Cleaner',
            'price': 2499.0,
            'category': 'Automotive',
            'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400',
            'description': 'Portable handheld vacuum with strong suction and LED light.',
            'rating': 4.4,
            'reviews': 4567,
            'in_stock': True,
            'source': 'Local Database'
        },
        {
            'id': 60,
            'name': 'Dash Cam 4K',
            'price': 7999.0,
            'category': 'Automotive',
            'image': 'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=400',
            'description': 'Dual camera dash cam with night vision and GPS tracking.',
            'rating': 4.6,
            'reviews': 2345,
            'in_stock': True,
            'source': 'Local Database'
        }
    ]

    # Add 80 more products (IDs 61-140)
    extra_product_specs = [
        ('Electronics', 'Smartphone Gimbal Stabilizer', 6999.0),
        ('Electronics', 'Mechanical Gaming Keyboard', 4599.0),
        ('Electronics', '27-inch QHD Monitor', 18999.0),
        ('Electronics', 'Portable SSD 1TB', 8499.0),
        ('Electronics', 'Wireless Charging Stand', 1999.0),
        ('Electronics', 'Smart Home Hub', 5999.0),
        ('Electronics', 'Action Camera 5K', 14999.0),
        ('Electronics', 'Noise-Cancel Earbuds', 7999.0),
        ('Electronics', 'Bluetooth Neckband Pro', 2499.0),
        ('Electronics', 'Webcam Full HD', 3299.0),
        ('Clothing', 'Casual Polo T-Shirt', 1499.0),
        ('Clothing', 'Slim Fit Chinos', 2299.0),
        ('Clothing', 'Women Denim Jeans', 2799.0),
        ('Clothing', 'Athletic Shorts', 1199.0),
        ('Clothing', 'Formal White Shirt', 1899.0),
        ('Clothing', 'Printed Hoodie', 2499.0),
        ('Clothing', 'Linen Summer Shirt', 2199.0),
        ('Clothing', 'Cotton Kurta Set', 1999.0),
        ('Clothing', 'Running Track Pants', 1699.0),
        ('Clothing', 'Classic Sneakers', 3299.0),
        ('Home & Garden', 'Smart WiFi Plug Set', 1799.0),
        ('Home & Garden', 'Air Fryer Digital 5L', 7999.0),
        ('Home & Garden', 'Memory Foam Pillow Pair', 2499.0),
        ('Home & Garden', 'Stainless Steel Cutlery Set', 1999.0),
        ('Home & Garden', 'Foldable Laundry Basket', 999.0),
        ('Home & Garden', 'Bathroom Organizer Rack', 1299.0),
        ('Home & Garden', 'Dining Table Runner Set', 899.0),
        ('Home & Garden', 'Cordless Hand Vacuum', 3499.0),
        ('Home & Garden', 'Blender Juicer Combo', 4599.0),
        ('Home & Garden', 'Aroma Diffuser', 1499.0),
        ('Beauty & Health', 'Vitamin C Face Serum', 799.0),
        ('Beauty & Health', 'Hair Straightener Ceramic', 2499.0),
        ('Beauty & Health', 'Protein Powder 1kg', 2199.0),
        ('Beauty & Health', 'Resistance Band Set', 1299.0),
        ('Beauty & Health', 'Smart Water Bottle', 1799.0),
        ('Beauty & Health', 'Handheld Facial Steamer', 1699.0),
        ('Beauty & Health', 'Electric Shaver Kit', 2999.0),
        ('Beauty & Health', 'Multivitamin Capsules', 699.0),
        ('Beauty & Health', 'Posture Corrector Belt', 999.0),
        ('Beauty & Health', 'Foam Roller Pro', 1499.0),
        ('Sports & Outdoors', 'Adjustable Dumbbell Set', 9999.0),
        ('Sports & Outdoors', 'Cricket Bat English Willow', 5999.0),
        ('Sports & Outdoors', 'Badminton Racket Pair', 2499.0),
        ('Sports & Outdoors', 'Cycling Helmet', 1999.0),
        ('Sports & Outdoors', 'Sports Water Bottle', 699.0),
        ('Sports & Outdoors', 'Skipping Rope Speed', 599.0),
        ('Sports & Outdoors', 'Camping Sleeping Bag', 2999.0),
        ('Sports & Outdoors', 'Hiking Backpack 45L', 3999.0),
        ('Sports & Outdoors', 'Football Training Cone Set', 899.0),
        ('Sports & Outdoors', 'Table Tennis Kit', 1499.0),
        ('Books & Media', 'Productivity Book Bundle', 1299.0),
        ('Books & Media', 'Children Story Collection', 999.0),
        ('Books & Media', 'Wireless Podcast Microphone', 4499.0),
        ('Books & Media', 'Beginner Piano Keyboard', 10999.0),
        ('Books & Media', 'Tripod Stand 72-inch', 1699.0),
        ('Books & Media', 'Photo Editing Course Pack', 2499.0),
        ('Books & Media', 'Noise Isolation Studio Headphones', 5999.0),
        ('Books & Media', 'Travel Documentary Box Set', 1799.0),
        ('Books & Media', 'Smart Notebook Reusable', 1499.0),
        ('Books & Media', 'Compact Binoculars', 2899.0),
        ('Toys & Games', 'STEM Robotics Kit', 3999.0),
        ('Toys & Games', 'Magnetic Building Tiles', 2299.0),
        ('Toys & Games', 'RC Drone for Kids', 4999.0),
        ('Toys & Games', 'Chess Tournament Board', 1499.0),
        ('Toys & Games', 'Kids Art Craft Box', 999.0),
        ('Toys & Games', 'Mini Basketball Hoop Set', 1299.0),
        ('Toys & Games', 'Strategy Card Game', 799.0),
        ('Toys & Games', 'Plush Toy Combo Pack', 1199.0),
        ('Toys & Games', 'Science Experiment Lab', 1899.0),
        ('Toys & Games', 'Educational Flash Cards', 599.0),
        ('Automotive', 'Car Phone Mount Magnetic', 699.0),
        ('Automotive', 'Tire Inflator Portable', 2499.0),
        ('Automotive', 'Seat Cover Premium Set', 3499.0),
        ('Automotive', 'Car Air Freshener Gel', 399.0),
        ('Automotive', 'Motorcycle Riding Gloves', 1299.0),
        ('Automotive', 'Car Jump Starter Kit', 5999.0),
        ('Automotive', 'Bike Mobile Holder', 499.0),
        ('Automotive', 'Pressure Washer Gun', 2199.0),
        ('Automotive', 'Car Sunshade Foldable', 799.0),
        ('Automotive', 'Emergency Roadside Tool Kit', 1999.0),
    ]

    next_id = len(products) + 1
    for idx, (category, name, price) in enumerate(extra_product_specs):
        products.append({
            'id': next_id + idx,
            'name': name,
            'price': price,
            'category': category,
            'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
            'description': f'High-quality {name.lower()} for everyday use and reliable performance.',
            'rating': 4.4 + ((idx % 5) * 0.1),
            'reviews': 120 + (idx * 13),
            'in_stock': True,
            'source': 'Local Database'
        })

    # Add 100 more products with category-specific images (IDs 141-240)
    category_image_map = {
        'Electronics': [
            'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400',
            'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400',
            'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400'
        ],
        'Clothing': [
            'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400',
            'https://images.unsplash.com/photo-1445205170230-053b83016050?w=400',
            'https://images.unsplash.com/photo-1467043153537-a4fba2cd39ef?w=400'
        ],
        'Home & Garden': [
            'https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=400',
            'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400',
            'https://images.unsplash.com/photo-1472220625704-91e1462799b2?w=400'
        ],
        'Beauty & Health': [
            'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400',
            'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400',
            'https://images.unsplash.com/photo-1556229010-aa3f7ff66b24?w=400'
        ],
        'Sports & Outdoors': [
            'https://images.unsplash.com/photo-1517649763962-0c623066013b?w=400',
            'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400',
            'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=400'
        ],
        'Books & Media': [
            'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400',
            'https://images.unsplash.com/photo-1489515217757-5fd1be406fef?w=400',
            'https://images.unsplash.com/photo-1544717305-2782549b5136?w=400'
        ],
        'Toys & Games': [
            'https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=400',
            'https://images.unsplash.com/photo-1610890716171-6b1c9f2bd40c?w=400',
            'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400'
        ],
        'Automotive': [
            'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=400',
            'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400',
            'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=400'
        ]
    }

    additional_100_specs = [
        ('Electronics', 'Smart Speaker Mini', 3499.0), ('Electronics', 'USB-C Docking Station', 5999.0),
        ('Electronics', 'Wireless Presenter Remote', 1299.0), ('Electronics', 'Tablet Keyboard Case', 2799.0),
        ('Electronics', 'Gaming Mouse RGB', 2199.0), ('Electronics', '4K Streaming Stick', 4999.0),
        ('Electronics', 'Smart Doorbell Camera', 8999.0), ('Electronics', 'Laptop Cooling Pad', 1499.0),
        ('Electronics', 'Portable Bluetooth Projector', 12999.0), ('Electronics', 'Ergonomic Vertical Mouse', 1999.0),
        ('Electronics', 'WiFi Range Extender', 2499.0), ('Electronics', 'Smart Fitness Band', 3299.0),
        ('Electronics', 'Type-C Fast Charger 65W', 1899.0),
        ('Clothing', 'Cotton Crew Neck Tee', 999.0), ('Clothing', 'Women Floral Top', 1399.0),
        ('Clothing', 'Men Classic Blazer', 4999.0), ('Clothing', 'Athleisure Joggers', 1899.0),
        ('Clothing', 'Winter Beanie Cap', 699.0), ('Clothing', 'Sports Compression Tee', 1299.0),
        ('Clothing', 'Chiffon Scarf Premium', 899.0), ('Clothing', 'Cargo Pants Utility', 2199.0),
        ('Clothing', 'Leather Belt Formal', 999.0), ('Clothing', 'Ankle Socks Pack of 5', 599.0),
        ('Clothing', 'Women Cardigan Knit', 1999.0), ('Clothing', 'Rain Jacket Waterproof', 2599.0),
        ('Clothing', 'Slip-On Canvas Shoes', 1799.0),
        ('Home & Garden', 'Ceramic Dinner Set 18pc', 2999.0), ('Home & Garden', 'Vacuum Storage Bags', 899.0),
        ('Home & Garden', 'Microfiber Mop Set', 1499.0), ('Home & Garden', 'LED Desk Lamp', 1699.0),
        ('Home & Garden', 'Wall Clock Minimal', 1299.0), ('Home & Garden', 'Bamboo Storage Organizer', 1599.0),
        ('Home & Garden', 'Bathroom Anti-Slip Mat', 699.0), ('Home & Garden', 'Digital Kitchen Scale', 1199.0),
        ('Home & Garden', 'Stainless Water Bottle 1L', 899.0), ('Home & Garden', 'Electric Kettle 1.8L', 1999.0),
        ('Home & Garden', 'Compact Shoe Rack', 1899.0), ('Home & Garden', 'Curtain Blackout Pair', 2299.0),
        ('Home & Garden', 'Non-Stick Tawa Pan', 1399.0),
        ('Beauty & Health', 'Aloe Vera Gel', 399.0), ('Beauty & Health', 'Sunscreen SPF 50', 699.0),
        ('Beauty & Health', 'Hair Serum Smoothening', 599.0), ('Beauty & Health', 'Beard Grooming Kit', 1499.0),
        ('Beauty & Health', 'Nail Care Set', 799.0), ('Beauty & Health', 'Organic Lip Balm Pack', 499.0),
        ('Beauty & Health', 'Digital Thermometer', 699.0), ('Beauty & Health', 'Blood Pressure Monitor', 2499.0),
        ('Beauty & Health', 'Hand Sanitizer Value Pack', 599.0), ('Beauty & Health', 'Yoga Stretch Strap', 499.0),
        ('Beauty & Health', 'Herbal Shampoo', 549.0), ('Beauty & Health', 'Face Wash Combo', 699.0),
        ('Beauty & Health', 'Sleep Mask Premium', 799.0),
        ('Sports & Outdoors', 'Kettlebell 12kg', 2999.0), ('Sports & Outdoors', 'Gym Gloves Breathable', 799.0),
        ('Sports & Outdoors', 'Badminton Shuttle Pack', 699.0), ('Sports & Outdoors', 'Cycling Water Bottle Cage', 499.0),
        ('Sports & Outdoors', 'Travel Trekking Poles', 2299.0), ('Sports & Outdoors', 'Football Shin Guards', 899.0),
        ('Sports & Outdoors', 'Tennis Balls Pack of 6', 999.0), ('Sports & Outdoors', 'Gym Resistance Tube Kit', 1199.0),
        ('Sports & Outdoors', 'Camping Lantern LED', 1299.0), ('Sports & Outdoors', 'Picnic Mat Waterproof', 899.0),
        ('Sports & Outdoors', 'Push-Up Board', 1499.0), ('Sports & Outdoors', 'Adjustable Ankle Weights', 1699.0),
        ('Sports & Outdoors', 'Sports Duffel Bag', 1999.0),
        ('Books & Media', 'Business Leadership Book Set', 1699.0), ('Books & Media', 'Beginner Sketching Kit', 1299.0),
        ('Books & Media', 'Audiobook Subscription Card', 999.0), ('Books & Media', 'Study Planner Journal', 499.0),
        ('Books & Media', 'Wireless Lavalier Mic', 2999.0), ('Books & Media', 'Story Book Box for Kids', 899.0),
        ('Books & Media', 'Language Learning Cards', 699.0), ('Books & Media', 'Documentary Blu-ray Pack', 1499.0),
        ('Books & Media', 'Art Pencil Set 48', 799.0), ('Books & Media', 'Notebook Set Premium', 599.0),
        ('Books & Media', 'Digital Metronome', 899.0), ('Books & Media', 'Acoustic Guitar Strings', 499.0),
        ('Books & Media', 'Camera Memory Card 128GB', 1899.0),
        ('Toys & Games', 'Kids Doctor Play Set', 1199.0), ('Toys & Games', 'Remote Dinosaur Toy', 1899.0),
        ('Toys & Games', 'Wooden Puzzle Blocks', 799.0), ('Toys & Games', 'UNO Card Pack Deluxe', 399.0),
        ('Toys & Games', 'Foam Dart Blaster', 1499.0), ('Toys & Games', 'Kids Piano Music Mat', 1299.0),
        ('Toys & Games', 'DIY Bracelet Making Kit', 899.0), ('Toys & Games', 'Mini Bowling Set', 699.0),
        ('Toys & Games', 'Alphabet Learning Board', 999.0), ('Toys & Games', 'Balance Bike for Kids', 3999.0),
        ('Toys & Games', 'Building Bricks 500pc', 1999.0), ('Toys & Games', 'Memory Match Card Game', 499.0),
        ('Toys & Games', 'Kids Telescope Starter', 1699.0),
        ('Automotive', 'Car Dashboard Cleaner Gel', 499.0), ('Automotive', 'Motorcycle Chain Lube', 699.0),
        ('Automotive', 'Car Trunk Organizer', 1499.0), ('Automotive', 'Dual USB Car Charger', 599.0),
        ('Automotive', 'Reflective Safety Triangle', 899.0), ('Automotive', 'Car Steering Wheel Cover', 999.0),
        ('Automotive', 'Vehicle OBD2 Scanner', 2999.0), ('Automotive', 'Motorbike Saddle Bag', 1899.0),
        ('Automotive', 'Car Wash Sponge Kit', 699.0), ('Automotive', 'Tire Pressure Gauge', 499.0),
        ('Automotive', 'Portable Car Fridge 12V', 8999.0), ('Automotive', 'Parking Sensor Kit', 3999.0),
        ('Automotive', 'Car Emergency Hammer Tool', 799.0)
    ]

    next_id = len(products) + 1
    for idx, (category, name, price) in enumerate(additional_100_specs[:100]):
        images = category_image_map.get(category) or [category_image_map['Electronics'][0]]
        image_url = images[idx % len(images)]
        products.append({
            'id': next_id + idx,
            'name': name,
            'price': price,
            'category': category,
            'image': image_url,
            'description': f'{name} with premium quality and reliable performance for daily use.',
            'rating': 4.2 + ((idx % 6) * 0.1),
            'reviews': 90 + (idx * 11),
            'in_stock': True,
            'source': 'Local Database'
        })

    # Add 100 more distinct products with individually matched real-world images (IDs 241-340)
    curated_100_products = [
        ('Electronics', 'Mirrorless Camera Kit', 52999.0, 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400'),
        ('Electronics', 'Smart Door Lock Pro', 10999.0, 'https://images.unsplash.com/photo-1558002038-1055907df827?w=400'),
        ('Electronics', 'USB Microphone Studio', 6499.0, 'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=400'),
        ('Electronics', 'Portable Power Station', 15999.0, 'https://images.unsplash.com/photo-1618560708927-464d67de4f29?w=400'),
        ('Electronics', 'Dual Band WiFi Router', 3999.0, 'https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=400'),
        ('Electronics', 'Smart Thermostat', 7999.0, 'https://images.unsplash.com/photo-1567925089135-6a5f88c32b2a?w=400'),
        ('Electronics', 'Bluetooth Turntable', 9499.0, 'https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=400'),
        ('Electronics', 'Drone Landing Pad Kit', 2299.0, 'https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=400'),
        ('Electronics', 'LED Ring Light 18-inch', 2899.0, 'https://images.unsplash.com/photo-1521579971123-1192931a1452?w=400'),
        ('Electronics', 'Portable Label Printer', 3499.0, 'https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=400'),
        ('Electronics', 'Electric Standing Desk Controller', 2599.0, 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=400'),
        ('Electronics', 'Smart Plug Energy Monitor', 1299.0, 'https://images.unsplash.com/photo-1558002038-1055907df827?w=400'),
        ('Electronics', 'Wireless HDMI Extender', 6999.0, 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400'),
        ('Clothing', 'Denim Shirt Casual Fit', 1699.0, 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400'),
        ('Clothing', 'Women Pleated Skirt', 1599.0, 'https://images.unsplash.com/photo-1583496661160-fb5886a13d77?w=400'),
        ('Clothing', 'Men Bomber Jacket', 3599.0, 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400'),
        ('Clothing', 'Athletic Running Tights', 1799.0, 'https://images.unsplash.com/photo-1517963879433-6ad2b056d712?w=400'),
        ('Clothing', 'Women Blazer Office Wear', 3299.0, 'https://images.unsplash.com/photo-1485462537746-965f33f7f6a7?w=400'),
        ('Clothing', 'Men Linen Trousers', 2199.0, 'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400'),
        ('Clothing', 'Kids Hoodie Fleece', 1399.0, 'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400'),
        ('Clothing', 'Leather Loafers', 3999.0, 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=400'),
        ('Clothing', 'Women Maxi Dress', 2799.0, 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400'),
        ('Clothing', 'Men Oxford Shoes', 4599.0, 'https://images.unsplash.com/photo-1531310197839-ccf54634509e?w=400'),
        ('Clothing', 'Cotton Night Suit Set', 1499.0, 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400'),
        ('Clothing', 'Woolen Shawl Premium', 1899.0, 'https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=400'),
        ('Clothing', 'Sports Windcheater', 2299.0, 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400'),
        ('Home & Garden', 'Ceramic Vase Set', 1399.0, 'https://images.unsplash.com/photo-1493666438817-866a91353ca9?w=400'),
        ('Home & Garden', 'Cotton Bath Towel Pack', 1199.0, 'https://images.unsplash.com/photo-1584622781867-244ac260f8b8?w=400'),
        ('Home & Garden', 'Wooden Cutting Board', 899.0, 'https://images.unsplash.com/photo-1514996937319-344454492b37?w=400'),
        ('Home & Garden', 'Scented Candle Gift Box', 1099.0, 'https://images.unsplash.com/photo-1602872030219-ad2b9b80f540?w=400'),
        ('Home & Garden', 'Cordless Table Lamp', 1799.0, 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400'),
        ('Home & Garden', 'Indoor Herb Planter', 1499.0, 'https://images.unsplash.com/photo-1463320726281-696a485928c7?w=400'),
        ('Home & Garden', 'Smart Smoke Detector', 3299.0, 'https://images.unsplash.com/photo-1574263867128-af66a10fda65?w=400'),
        ('Home & Garden', 'Premium Bedsheet Set', 2299.0, 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400'),
        ('Home & Garden', 'Dish Drying Rack Steel', 1599.0, 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400'),
        ('Home & Garden', 'Wall Shelf Floating', 1899.0, 'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=400'),
        ('Home & Garden', 'Vacuum Flask Set', 1299.0, 'https://images.unsplash.com/photo-1523362628745-0c100150b504?w=400'),
        ('Home & Garden', 'Home Tool Kit 50pc', 2499.0, 'https://images.unsplash.com/photo-1504148455328-c376907d081c?w=400'),
        ('Home & Garden', 'Anti-Fatigue Floor Mat', 999.0, 'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=400'),
        ('Beauty & Health', 'Hydrating Face Mist', 549.0, 'https://images.unsplash.com/photo-1571781565036-d3f759be73e4?w=400'),
        ('Beauty & Health', 'Professional Hair Trimmer', 2199.0, 'https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=400'),
        ('Beauty & Health', 'Vitamin E Body Lotion', 699.0, 'https://images.unsplash.com/photo-1556229174-5e42a09e45af?w=400'),
        ('Beauty & Health', 'Infrared Heating Pad', 1799.0, 'https://images.unsplash.com/photo-1581594693702-fbdc51b2763b?w=400'),
        ('Beauty & Health', 'Digital Weighing Machine', 1499.0, 'https://images.unsplash.com/photo-1511988617509-a57c8a288659?w=400'),
        ('Beauty & Health', 'Foaming Hand Wash Pack', 499.0, 'https://images.unsplash.com/photo-1583947582886-f40ec95dd752?w=400'),
        ('Beauty & Health', 'Hair Curling Wand', 1999.0, 'https://images.unsplash.com/photo-1522338140263-f46f5913618a?w=400'),
        ('Beauty & Health', 'Meditation Cushion', 1299.0, 'https://images.unsplash.com/photo-1514996550219-62672472d03b?w=400'),
        ('Beauty & Health', 'Daily Nutrition Tablets', 799.0, 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400'),
        ('Beauty & Health', 'Orthopedic Neck Pillow', 1699.0, 'https://images.unsplash.com/photo-1616627452218-9d6d527cb8e2?w=400'),
        ('Beauty & Health', 'Charcoal Face Mask', 599.0, 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=400'),
        ('Beauty & Health', 'Smart Jump Rope', 1299.0, 'https://images.unsplash.com/photo-1599058917765-a780eda07a3e?w=400'),
        ('Beauty & Health', 'Essential Oil Set', 999.0, 'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=400'),
        ('Sports & Outdoors', 'Adjustable Yoga Wheel', 1499.0, 'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=400'),
        ('Sports & Outdoors', 'Outdoor Picnic Backpack', 2699.0, 'https://images.unsplash.com/photo-1504280390368-397d85d89d5f?w=400'),
        ('Sports & Outdoors', 'Climbing Rope Training', 1999.0, 'https://images.unsplash.com/photo-1526481280695-3c469d734f23?w=400'),
        ('Sports & Outdoors', 'Skateboard Cruiser', 3499.0, 'https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=400'),
        ('Sports & Outdoors', 'Portable Hammock', 1799.0, 'https://images.unsplash.com/photo-1473448912268-2022ce9509d8?w=400'),
        ('Sports & Outdoors', 'Camping Cookware Set', 2399.0, 'https://images.unsplash.com/photo-1504851149312-5a0750b4969f?w=400'),
        ('Sports & Outdoors', 'Basketball Hoop Net', 899.0, 'https://images.unsplash.com/photo-1519861531473-920026393112?w=400'),
        ('Sports & Outdoors', 'Swim Cap and Goggles Set', 999.0, 'https://images.unsplash.com/photo-1560090995-01632a28895b?w=400'),
        ('Sports & Outdoors', 'Trekking Headlamp', 1299.0, 'https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?w=400'),
        ('Sports & Outdoors', 'Cycling Repair Tool Kit', 1199.0, 'https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=400'),
        ('Sports & Outdoors', 'Volleyball Match Ball', 1499.0, 'https://images.unsplash.com/photo-1612872087720-bb876e2e67d1?w=400'),
        ('Sports & Outdoors', 'Ab Roller Wheel', 999.0, 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400'),
        ('Sports & Outdoors', 'Folding Camping Chair', 2199.0, 'https://images.unsplash.com/photo-1504280390368-397d85d89d5f?w=400'),
        ('Books & Media', 'Photography Basics Guide', 899.0, 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=400'),
        ('Books & Media', 'Motivation Quotes Desk Calendar', 499.0, 'https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400'),
        ('Books & Media', 'Graphic Tablet Beginner', 7999.0, 'https://images.unsplash.com/photo-1587614382346-4ec70e388b28?w=400'),
        ('Books & Media', 'Podcast Audio Interface', 10999.0, 'https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=400'),
        ('Books & Media', 'History Documentary Collection', 1299.0, 'https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?w=400'),
        ('Books & Media', 'Songwriting Journal', 699.0, 'https://images.unsplash.com/photo-1455390582262-044cdead277a?w=400'),
        ('Books & Media', 'Portable E-Reading Light', 799.0, 'https://images.unsplash.com/photo-1513001900722-370f803f498d?w=400'),
        ('Books & Media', 'Camera Lens Cleaning Kit', 599.0, 'https://images.unsplash.com/photo-1512790182412-b19e6d62bc39?w=400'),
        ('Books & Media', 'Music Theory Workbook', 749.0, 'https://images.unsplash.com/photo-1461783436728-0a9217714694?w=400'),
        ('Books & Media', 'Educational Atlas Deluxe', 999.0, 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400'),
        ('Books & Media', 'Portable Audio Recorder', 4499.0, 'https://images.unsplash.com/photo-1603732551658-5fabbafa84eb?w=400'),
        ('Books & Media', 'Calligraphy Starter Set', 899.0, 'https://images.unsplash.com/photo-1455885666463-9d4f0f428f19?w=400'),
        ('Books & Media', 'Science Encyclopedia Set', 1399.0, 'https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400'),
        ('Toys & Games', 'Kids Kitchen Play Set', 1799.0, 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400'),
        ('Toys & Games', 'Electric RC Boat', 2999.0, 'https://images.unsplash.com/photo-1545558014-8692077e9b5c?w=400'),
        ('Toys & Games', 'Wooden Train Set', 2199.0, 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400'),
        ('Toys & Games', 'Jigsaw Puzzle Cityscape', 899.0, 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400'),
        ('Toys & Games', 'Kids Magic Trick Kit', 1299.0, 'https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=400'),
        ('Toys & Games', 'Remote Control Excavator', 3499.0, 'https://images.unsplash.com/photo-1594787318286-3d835c1d207f?w=400'),
        ('Toys & Games', 'Board Game Strategy Deluxe', 1499.0, 'https://images.unsplash.com/photo-1610890716171-6b1c9f2bd40c?w=400'),
        ('Toys & Games', 'Math Learning Cubes', 799.0, 'https://images.unsplash.com/photo-1602793048584-9ea3df6f7a55?w=400'),
        ('Toys & Games', 'Kids Building Engineer Kit', 1999.0, 'https://images.unsplash.com/photo-1515488764276-beab7607c1e6?w=400'),
        ('Toys & Games', 'Doll House Furniture Set', 1299.0, 'https://images.unsplash.com/photo-1585366119957-e9730b6d0f60?w=400'),
        ('Toys & Games', 'Foam Puzzle Floor Mat', 999.0, 'https://images.unsplash.com/photo-1516627145497-ae6968895b74?w=400'),
        ('Toys & Games', 'Kids Karaoke Microphone', 1499.0, 'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=400'),
        ('Toys & Games', 'Educational Solar Robot', 2499.0, 'https://images.unsplash.com/photo-1561144257-e32e8efc6c4f?w=400'),
        ('Automotive', 'Rear View Mirror Camera', 6999.0, 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400'),
        ('Automotive', 'Portable Car Air Purifier', 2999.0, 'https://images.unsplash.com/photo-1502877338535-766e1452684a?w=400'),
        ('Automotive', 'Bike Helmet Full Face', 3499.0, 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400'),
        ('Automotive', 'Car Floor Mat 5D', 2499.0, 'https://images.unsplash.com/photo-1493238792000-8113da705763?w=400'),
        ('Automotive', 'LED Fog Light Pair', 1799.0, 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400'),
        ('Automotive', 'Motorcycle Phone Charger', 899.0, 'https://images.unsplash.com/photo-1469285994282-454ceb49e63a?w=400'),
        ('Automotive', 'Car Dent Repair Kit', 1299.0, 'https://images.unsplash.com/photo-1487754180451-c456f719a1fc?w=400'),
        ('Automotive', 'Vehicle Tyre Shine Spray', 499.0, 'https://images.unsplash.com/photo-1605152276897-4f618f831968?w=400'),
        ('Automotive', 'Car Vacuum and Blower', 2799.0, 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400'),
        ('Automotive', 'Bike Saddle Cushion Gel', 999.0, 'https://images.unsplash.com/photo-1508973379184-7517410fb0d8?w=400'),
        ('Automotive', 'Car Emergency First Aid Kit', 1499.0, 'https://images.unsplash.com/photo-1508973379184-7517410fb0d8?w=400'),
        ('Automotive', 'Snow Foam Car Wash Gun', 1999.0, 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=400'),
        ('Automotive', 'Reflective Bike Jacket', 1799.0, 'https://images.unsplash.com/photo-1518002171953-a080ee817e1f?w=400'),
    ]

    next_id = len(products) + 1
    for idx, (category, name, price, image_url) in enumerate(curated_100_products[:100]):
        products.append({
            'id': next_id + idx,
            'name': name,
            'price': price,
            'category': category,
            'image': image_url,
            'description': f'{name} from trusted brands, selected for quality and real-world performance.',
            'rating': 4.3 + ((idx % 5) * 0.1),
            'reviews': 110 + (idx * 9),
            'in_stock': True,
            'source': 'Local Database'
        })
    
    return products

def populate_products():
    """Populate the database with sample products"""
    products_data = get_local_products()
    
    for product_data in products_data:
        # Skip if product with this name already exists
        if Product.query.filter_by(name=product_data['name']).first():
            continue
            
        product = Product(
            name=product_data['name'],
            description=product_data.get('description', ''),
            price=product_data['price'],
            category=product_data['category'],
            image_url=product_data.get('image', ''),
            stock_quantity=product_data.get('stock_quantity', 100),
            rating=product_data.get('rating', 0),
            review_count=product_data.get('reviews', 0),
            is_active=product_data.get('in_stock', True)
        )
        db.session.add(product)
    
    db.session.commit()

# Database initialization
def create_tables():
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(email='admin@cartify.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@cartify.com',
                first_name='Admin',
                last_name='User',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin@cartify.com / admin123")
            
            # Create loyalty points for admin
            loyalty = LoyaltyPoints(user_id=admin.id, points=1000, lifetime_points=1000, tier='gold')
            db.session.add(loyalty)
            
            # Create language preference for admin
            lang_pref = UserLanguagePreference(user_id=admin.id, language_code='en')
            db.session.add(lang_pref)
            
            # Create notification preferences for admin
            notif_pref = NotificationPreference(user_id=admin.id)
            db.session.add(notif_pref)
            db.session.commit()
        
        # Create demo user if it doesn't exist
        demo = User.query.filter_by(email='demo@cartify.com').first()
        if not demo:
            demo = User(
                username='demo',
                email='demo@cartify.com',
                first_name='Demo',
                last_name='User',
                email_verified=True
            )
            demo.set_password('demo123')
            db.session.add(demo)
            db.session.commit()
            print("Demo user created: demo@cartify.com / demo123")
            
            # Create loyalty points for demo user
            loyalty = LoyaltyPoints(user_id=demo.id, points=500, lifetime_points=500, tier='silver')
            db.session.add(loyalty)
            
            # Create preferences
            lang_pref = UserLanguagePreference(user_id=demo.id, language_code='en')
            notif_pref = NotificationPreference(user_id=demo.id)
            db.session.add(lang_pref)
            db.session.add(notif_pref)
            db.session.commit()
        
        # Populate products if database is empty
        if Product.query.count() == 0:
            populate_products()
            print("Products populated from local data")
        
        # Initialize chatbot intents if empty
        if ChatbotIntentClassification.query.count() == 0:
            intents = [
                {
                    'intent_name': 'product_search',
                    'intent_description': 'User wants to search for products',
                    'example_questions': json.dumps(['Find shirts', 'Show me electronics', 'I need shoes']),
                    'response_template': 'Let me help you find products. What are you looking for?',
                    'requires_product_id': False,
                    'requires_user_id': False,
                    'priority': 10
                },
                {
                    'intent_name': 'order_status',
                    'intent_description': 'User wants to check order status',
                    'example_questions': json.dumps(['Where is my order?', 'Track my order', 'Order status']),
                    'response_template': 'Let me check your order status. Please provide your order number.',
                    'requires_product_id': False,
                    'requires_user_id': True,
                    'priority': 9
                },
                {
                    'intent_name': 'product_recommendation',
                    'intent_description': 'User wants product recommendations',
                    'example_questions': json.dumps(['Recommend something', 'What should I buy?', 'Suggestions']),
                    'response_template': 'Based on your preferences, here are some recommendations...',
                    'requires_product_id': False,
                    'requires_user_id': True,
                    'priority': 8
                },
                {
                    'intent_name': 'cart_management',
                    'intent_description': 'User wants to manage their cart',
                    'example_questions': json.dumps(['Add to cart', 'Remove from cart', 'View cart']),
                    'response_template': 'I can help you manage your cart.',
                    'requires_product_id': True,
                    'requires_user_id': True,
                    'priority': 7
                },
                {
                    'intent_name': 'account',
                    'intent_description': 'User has account-related questions',
                    'example_questions': json.dumps(['Change password', 'Update profile', 'My account']),
                    'response_template': 'I can help with your account. What would you like to do?',
                    'requires_product_id': False,
                    'requires_user_id': True,
                    'priority': 6
                },
                {
                    'intent_name': 'general',
                    'intent_description': 'General conversation',
                    'example_questions': json.dumps(['Hello', 'Hi', 'Help']),
                    'response_template': 'How can I assist you today?',
                    'requires_product_id': False,
                    'requires_user_id': False,
                    'priority': 1
                }
            ]
            
            for intent_data in intents:
                intent = ChatbotIntentClassification(**intent_data)
                db.session.add(intent)
            
            db.session.commit()
            print("Chatbot intents initialized")
        
        # Create language preferences for existing users without them
        users_without_lang = User.query.outerjoin(UserLanguagePreference).filter(UserLanguagePreference.id == None).all()
        for user in users_without_lang:
            lang_pref = UserLanguagePreference(user_id=user.id, language_code='en')
            db.session.add(lang_pref)
        if users_without_lang:
            db.session.commit()
            print(f"Created language preferences for {len(users_without_lang)} users")
        
        # Create notification preferences for existing users without them
        users_without_notif = User.query.outerjoin(NotificationPreference).filter(NotificationPreference.id == None).all()
        for user in users_without_notif:
            notif_pref = NotificationPreference(user_id=user.id)
            db.session.add(notif_pref)
        if users_without_notif:
            db.session.commit()
            print(f"Created notification preferences for {len(users_without_notif)} users")
        
        # Create loyalty points for existing users without them
        users_without_loyalty = User.query.outerjoin(LoyaltyPoints).filter(LoyaltyPoints.id == None).all()
        for user in users_without_loyalty:
            loyalty = LoyaltyPoints(user_id=user.id)
            db.session.add(loyalty)
        if users_without_loyalty:
            db.session.commit()
            print(f"Created loyalty points for {len(users_without_loyalty)} users")

# Initialize database
create_tables()

@app.route('/')
def home():
    # Get featured products from database
    featured_products = Product.query.filter_by(is_active=True).limit(8).all()
    # Convert to dict format for template compatibility
    products_data = [product.to_dict() for product in featured_products]
    return render_template('home.html', products=products_data)

@app.route('/products')
def products_page():
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'name')
    price_min = request.args.get('price_min', '')
    price_max = request.args.get('price_max', '')
    
    # Start with active products
    query = Product.query.filter_by(is_active=True)
    
    # Apply filters
    if category:
        query = query.filter(Product.category.ilike(f'%{category}%'))
    
    if search:
        query = query.filter(
            (Product.name.ilike(f'%{search}%')) | 
            (Product.description.ilike(f'%{search}%'))
        )
    
    if price_min:
        try:
            min_price = float(price_min)
            query = query.filter(Product.price >= min_price)
        except ValueError:
            pass
    
    if price_max:
        try:
            max_price = float(price_max)
            query = query.filter(Product.price <= max_price)
        except ValueError:
            pass
    
    # Apply sorting with stable ordering to prevent number decreasing
    if sort_by == 'price_low':
        query = query.order_by(Product.price.asc(), Product.id.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Product.price.desc(), Product.id.asc())
    elif sort_by == 'rating':
        query = query.order_by(Product.rating.desc(), Product.id.asc())
    elif sort_by == 'name':
        query = query.order_by(Product.name.asc(), Product.id.asc())
    elif sort_by == 'newest':
        query = query.order_by(Product.created_at.desc(), Product.id.desc())
    elif sort_by == 'oldest':
        query = query.order_by(Product.created_at.asc(), Product.id.asc())
    else:
        # Default sort by name with stable ordering
        query = query.order_by(Product.name.asc(), Product.id.asc())
    
    # Fetch all matching products from database
    filtered_products = query.all()
    products_data = [product.to_dict() for product in filtered_products]
    
    # Get categories for filter dropdown
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template(
        'products.html',
        products=products_data,
        categories=categories,
        current_category=category,
        current_search=search,
        current_sort=sort_by,
        price_min=price_min,
        price_max=price_max,
        total_products=len(products_data),
        current_page=1,
        total_pages=1
    )

@app.route('/api/products')
def api_products():
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    limit = request.args.get('limit')

    # Query products from database
    query = Product.query.filter_by(is_active=True)

    if category:
        query = query.filter(Product.category.ilike(f'%{category}%'))

    if search:
        query = query.filter(
            (Product.name.ilike(f'%{search}%')) |
            (Product.description.ilike(f'%{search}%'))
        )

    if limit:
        try:
            limit = int(limit)
            filtered_products = query.limit(limit).all()
        except ValueError:
            filtered_products = query.all()
            limit = len(filtered_products)
    else:
        filtered_products = query.all()
        limit = len(filtered_products)
    products_data = [product.to_dict() for product in filtered_products]

    return jsonify({
        'products': products_data,
        'total': len(products_data),
        'limit': limit
    })

@app.route('/api/categories')
def api_categories():
    categories = db.session.query(Product.category).distinct().all()
    categories = sorted([cat[0] for cat in categories])
    return jsonify({'categories': categories})

@app.route('/api/refresh-products')
def refresh_products():
    try:
        # Re-sync product catalog from local source without deleting existing rows.
        before_count = Product.query.count()
        populate_products()
        after_count = Product.query.count()
        product_count = after_count
        added_count = max(0, after_count - before_count)

        return jsonify({
            'success': True,
            'message': f'Catalog synced successfully. Total products: {product_count} (added {added_count}).',
            'product_count': product_count,
            'added': added_count
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error refreshing products: {str(e)}'
        }), 500


@app.route('/api/products/add', methods=['POST'])
@admin_required
def add_product():
    """Add a new product to the database (Admin only)"""
    data = request.get_json()
    
    try:
        product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            category=data['category'],
            image_url=data.get('image_url', ''),
            stock_quantity=int(data.get('stock_quantity', 100)),
            rating=float(data.get('rating', 0)),
            review_count=int(data.get('review_count', 0)),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Product "{product.name}" added successfully!',
            'product': product.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error adding product: {str(e)}'
        }), 400

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('products_page'))

    # Fetch related products (e.g., from the same category, excluding the current product)
    related_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product_id
    ).limit(4).all()

    return render_template('product_detail.html', product=product, related_products=related_products)


@app.route('/cart')
@login_required
def cart_page():
    user = get_current_user()
    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    
    cart_data = []
    total = 0
    
    for item in cart_items:
        item_total = item.product.price * item.quantity
        cart_data.append({
            'product': item.product.to_dict(),
            'quantity': item.quantity,
            'total': item_total
        })
        total += item_total
    
    return render_template('cart.html', cart_items=cart_data, total=total)

@app.route('/checkout')
@login_required
def checkout():
    user = get_current_user()
    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    
    if not cart_items:
        flash('Your cart is empty. Add items before checking out.', 'error')
        return redirect(url_for('cart_page'))
    
    cart_data = []
    total = 0
    
    for item in cart_items:
        item_total = item.product.price * item.quantity
        cart_data.append({
            'product': item.product.to_dict(),
            'quantity': item.quantity,
            'total': item_total
        })
        total += item_total

    indian_states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
        "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",
        "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
        "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
    ]

    return render_template('checkout.html', cart_items=cart_data, total=total, indian_states=indian_states)

@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    user = get_current_user()
    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    
    if not cart_items:
        return jsonify({'success': False, 'message': 'Your cart is empty.'}), 400
    
    # Create order
    order_number = f'ORD-{random.randint(100000, 999999)}'
    order_total = sum(item.product.price * item.quantity for item in cart_items)
    tax_amount = order_total * 0.18
    shipping_cost = 0 # Default shipping cost

    # Extract shipping address from request.json
    shipping_address_data = request.json.get('shippingAddress', {})
    shipping_method = request.json.get('shippingMethod', 'standard')
    payment_method = request.json.get('paymentMethod', 'card')
    
    # Calculate shipping cost based on selected method
    if shipping_method == 'express':
        shipping_cost = 829
    elif shipping_method == 'overnight':
        shipping_cost = 1659

    order = Order(
        order_number=order_number,
        user_id=user.id,
        total_amount=order_total + tax_amount + shipping_cost,
        shipping_address=shipping_address_data.get('address', ''),
        shipping_city=shipping_address_data.get('city', ''),
        shipping_state=shipping_address_data.get('state', ''),
        shipping_pincode=shipping_address_data.get('zipCode', ''),
        payment_method=payment_method,
        tax_amount=tax_amount,
        shipping_cost=shipping_cost,
        notes=request.json.get('orderNotes', '')
    )
    
    db.session.add(order)
    db.session.flush()  # Get order ID
    
    # Create order items
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        db.session.add(order_item)
    
    # Clear cart
    CartItem.query.filter_by(user_id=user.id).delete()
    
    # Award loyalty points (1 point per ₹100 spent)
    loyalty = LoyaltyPoints.query.filter_by(user_id=user.id).first()
    if not loyalty:
        loyalty = LoyaltyPoints(user_id=user.id)
        db.session.add(loyalty)
        db.session.flush()
    
    # Calculate points with tier multiplier
    base_points = int(order_total / 100)
    benefits = loyalty.get_tier_benefits()
    bonus_multiplier = benefits.get('points_multiplier', 1)
    total_points = int(base_points * bonus_multiplier)
    
    loyalty.add_points(total_points, f'Order #{order_number}')
    
    db.session.commit()
    
    # Build success message with points info
    points_message = f" You earned {total_points} loyalty points!"
    if bonus_multiplier > 1:
        points_message += f" ({bonus_multiplier}x {loyalty.tier.title()} bonus)"
    
    return jsonify({
        'success': True,
        'message': f'Order #{order_number} placed successfully! Total: ₹{int(order_total + tax_amount + shipping_cost):,}.{points_message}'
    })

@app.route('/orders')
@login_required
def order_tracking():
    user = get_current_user()
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    return render_template('order_tracking.html', orders=orders)


@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = int(data.get('product_id'))
    quantity = int(data.get('quantity', 1))
    
    user = get_current_user()
    product = Product.query.get_or_404(product_id)
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(
        user_id=user.id, 
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Added to cart successfully!'})

@app.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    data = request.get_json()
    product_id = int(data.get('product_id'))
    quantity = int(data.get('quantity', 0))
    
    user = get_current_user()
    cart_item = CartItem.query.filter_by(
        user_id=user.id, 
        product_id=product_id
    ).first()
    
    if quantity <= 0:
        if cart_item:
            db.session.delete(cart_item)
    else:
        if cart_item:
            cart_item.quantity = quantity
        else:
            cart_item = CartItem(
                user_id=user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Cart updated successfully!'})



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()

        if not username or not email or not password or not first_name or not last_name:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('signup'))

        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('signup'))

        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return redirect(url_for('signup'))

        if confirm_password and password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('signup'))

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('login'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken. Please choose another.', 'error')
            return redirect(url_for('signup'))

        try:
            # Create new user directly
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                email_verified=True  # Email automatically verified on signup
            )
            user.set_password(password)

            db.session.add(user)
            db.session.flush()  # Get user ID

            # Create loyalty points for new user with welcome bonus
            loyalty = LoyaltyPoints(
                user_id=user.id,
                points=100,
                lifetime_points=100,
                tier='bronze'
            )
            db.session.add(loyalty)
            db.session.flush()

            welcome_txn = LoyaltyTransaction(
                loyalty_id=loyalty.id,
                points=100,
                type='bonus',
                reason='Welcome bonus for new member'
            )
            db.session.add(welcome_txn)

            # Create language preference (default to English)
            lang_pref = UserLanguagePreference(user_id=user.id, language_code='en')
            db.session.add(lang_pref)

            # Create notification preferences
            notif_pref = NotificationPreference(user_id=user.id)
            db.session.add(notif_pref)

            db.session.commit()

            flash('Account created successfully! You received 100 welcome bonus points. Please log in.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            print(f"Signup error: {e}")
            flash('An error occurred while creating your account. Please try again.', 'error')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        
        flash('Invalid email or password.', 'error')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))


# Newsletter Subscribers (in-memory storage for now)
newsletter_subscribers = set()

@app.route('/api/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Subscribe to newsletter"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400
    
    # Simple email validation
    import re
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({'success': False, 'message': 'Please enter a valid email address'}), 400
    
    if email in newsletter_subscribers:
        return jsonify({'success': False, 'message': 'You are already subscribed!'}), 400
    
    newsletter_subscribers.add(email)
    print(f"New subscriber: {email}")
    
    return jsonify({
        'success': True, 
        'message': 'Thank you for subscribing to our newsletter!'
    })


@app.route('/api/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile information"""
    user = get_current_user()
    data = request.get_json()
    
    try:
        # Update fields if provided
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'email' in data and data['email'] != user.email:
            # Check if email is already taken
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user.id:
                return jsonify({'success': False, 'message': 'Email already in use'}), 400
            user.email = data['email']
        
        # Update address fields
        if 'address' in data:
            user.address = data['address']
        if 'city' in data:
            user.city = data['city']
        if 'state' in data:
            user.state = data['state']
        if 'pincode' in data:
            user.pincode = data['pincode']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully!',
            'user': user.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/api/profile/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    user = get_current_user()
    data = request.get_json()
    
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({'success': False, 'message': 'Both current and new password required'}), 400
    
    if not user.check_password(current_password):
        return jsonify({'success': False, 'message': 'Current password is incorrect'}), 400
    
    if len(new_password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
    
    try:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Password changed successfully!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/profile')
@login_required
def profile():
    user = get_current_user()
    
    # Get loyalty points info
    loyalty = LoyaltyPoints.query.filter_by(user_id=user.id).first()
    if not loyalty:
        loyalty = LoyaltyPoints(user_id=user.id)
        db.session.add(loyalty)
        db.session.commit()
    
    # Get recent transactions
    transactions = LoyaltyTransaction.query.join(LoyaltyPoints).filter(
        LoyaltyPoints.user_id == user.id
    ).order_by(LoyaltyTransaction.created_at.desc()).limit(10).all()
    
    # Get user's orders
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('profile.html', 
                         user=user,
                         loyalty=loyalty,
                         transactions=transactions,
                         orders=orders)


# ==================== LOYALTY POINTS API ROUTES ====================

@app.route('/api/loyalty')
@login_required
def get_loyalty_info():
    """Get current user's loyalty points information"""
    user = get_current_user()
    loyalty = LoyaltyPoints.query.filter_by(user_id=user.id).first()
    
    if not loyalty:
        loyalty = LoyaltyPoints(user_id=user.id)
        db.session.add(loyalty)
        db.session.commit()
    
    return jsonify({
        'success': True,
        'loyalty': loyalty.to_dict()
    })


@app.route('/api/loyalty/transactions')
@login_required
def get_loyalty_transactions():
    """Get loyalty points transaction history"""
    user = get_current_user()
    loyalty = LoyaltyPoints.query.filter_by(user_id=user.id).first()
    
    if not loyalty:
        return jsonify({'success': True, 'transactions': []})
    
    transactions = LoyaltyTransaction.query.filter_by(
        loyalty_id=loyalty.id
    ).order_by(LoyaltyTransaction.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'transactions': [t.to_dict() for t in transactions]
    })


@app.route('/api/loyalty/redeem', methods=['POST'])
@login_required
def redeem_loyalty_points():
    """Redeem loyalty points for discount"""
    user = get_current_user()
    data = request.get_json()
    points_to_redeem = data.get('points', 0)
    
    if points_to_redeem < 100:
        return jsonify({
            'success': False,
            'message': 'Minimum 100 points required for redemption'
        }), 400
    
    loyalty = LoyaltyPoints.query.filter_by(user_id=user.id).first()
    
    if not loyalty or loyalty.points < points_to_redeem:
        return jsonify({
            'success': False,
            'message': 'Insufficient points balance'
        }), 400
    
    # Calculate discount (1 point = ₹0.50)
    discount_amount = points_to_redeem * 0.5
    
    if loyalty.redeem_points(points_to_redeem, f'Redeemed for ₹{discount_amount:.0f} discount'):
        return jsonify({
            'success': True,
            'message': f'Successfully redeemed {points_to_redeem} points for ₹{discount_amount:.0f} discount!',
            'discount': discount_amount,
            'remaining_points': loyalty.points
        })
    
    return jsonify({
        'success': False,
        'message': 'Failed to redeem points'
    }), 400


# ==================== CHATBOT API ROUTES ====================

import uuid
import re

def search_products_in_db(query, limit=3):
    """Search products in database and return formatted results"""
    search_term = f'%{query}%'
    products = Product.query.filter(
        (Product.name.ilike(search_term)) | 
        (Product.description.ilike(search_term)) |
        (Product.category.ilike(search_term))
    ).filter_by(is_active=True).limit(limit).all()
    
    if products:
        result = "I found these products for you:\n\n"
        for p in products:
            result += f"• {p.name} - ₹{int(p.price):,}\n  {p.description[:80]}...\n\n"
        result += "Click on any product to view details and purchase!"
        return result
    return None

def get_product_recommendations(category=None, max_price=None):
    """Get product recommendations based on category or price"""
    query = Product.query.filter_by(is_active=True)
    
    if category:
        query = query.filter(Product.category.ilike(f'%{category}%'))
    if max_price:
        try:
            query = query.filter(Product.price <= float(max_price))
        except:
            pass
    
    products = query.order_by(Product.rating.desc()).limit(3).all()
    
    if products:
        result = f"Here are some great recommendations{' in ' + category if category else ''}:\n\n"
        for p in products:
            result += f"⭐ {p.name}\n   Price: ₹{int(p.price):,} | Rating: {p.rating}/5\n\n"
        return result
    return None

def get_chatbot_response(message, user=None):
    """
    Enhanced chatbot with real-world scenarios and attractive responses
    """
    message_lower = message.lower().strip()
    
    # Initialize enhanced chatbot
    chatbot = enhanced_chatbot()
    
    # Set user context
    if user:
        chatbot.user_id = user.id
        chatbot.session_id = str(uuid.uuid4())
    # Product search - specific product queries
    product_keywords = ['find', 'search', 'looking for', 'show me', 'do you have', 'where can i find']
    if any(keyword in message_lower for keyword in product_keywords):
        # Extract search term
        search_term = message_lower
        for keyword in product_keywords:
            search_term = search_term.replace(keyword, '')
        search_term = search_term.strip()
        
        if search_term:
            result = search_products_in_db(search_term)
            if result:
                return result
            else:
                return f"I couldn't find any products matching '{search_term}'. Try browsing our Products page or search with different keywords. We have 60+ products across 8 categories!"
    
    # Recommendations
    if any(word in message_lower for word in ['recommend', 'suggestion', 'best', 'top rated', 'popular']):
        category = None
        if 'electronics' in message_lower:
            category = 'Electronics'
        elif 'clothing' in message_lower or 'clothes' in message_lower:
            category = 'Clothing'
        elif 'home' in message_lower:
            category = 'Home'
        elif 'beauty' in message_lower:
            category = 'Beauty'
        elif 'sports' in message_lower:
            category = 'Sports'
        elif 'toy' in message_lower or 'game' in message_lower:
            category = 'Toys'
        
        result = get_product_recommendations(category)
        if result:
            return result
        return "Check out our bestsellers on the homepage! We have top-rated products across all categories with customer reviews to help you decide."
    
    # Cheap/affordable products
    if any(word in message_lower for word in ['cheap', 'affordable', 'budget', 'under', 'less than', 'below']):
        # Extract price
        price_match = re.search(r'(\d+)', message_lower)
        if price_match:
            max_price = price_match.group(1)
            result = get_product_recommendations(max_price=max_price)
            if result:
                return f"Here are products under ₹{max_price}:\n\n" + result
        
        affordable = Product.query.filter(Product.price <= 2000).filter_by(is_active=True).order_by(Product.price.asc()).limit(3).all()
        if affordable:
            result = "Here are some affordable options under ₹2,000:\n\n"
            for p in affordable:
                result += f"• {p.name} - ₹{int(p.price):,}\n"
            return result
    
    # Expensive/premium products
    if any(word in message_lower for word in ['expensive', 'premium', 'high end', 'luxury', 'best quality']):
        premium = Product.query.filter(Product.price >= 40000).filter_by(is_active=True).order_by(Product.rating.desc()).limit(3).all()
        if premium:
            result = "Here are our premium products:\n\n"
            for p in premium:
                result += f"💎 {p.name} - ₹{int(p.price):,}\n   Rating: {p.rating}/5\n\n"
            return result
    
    # Price check for specific items
    price_queries = ['how much is', 'price of', 'cost of', 'what is the price']
    if any(query in message_lower for query in price_queries):
        # Try to extract product name
        for query in price_queries:
            if query in message_lower:
                product_name = message_lower.replace(query, '').strip()
                if product_name:
                    product = Product.query.filter(Product.name.ilike(f'%{product_name}%')).first()
                    if product:
                        return f"The {product.name} is priced at ₹{int(product.price):,}. It has a {product.rating}/5 star rating from {product.review_count} reviews. Would you like to add it to your cart?"
        
        return "Please specify a product name to check its price. For example: 'How much is the iPhone?' or 'Price of yoga mat'"
    
    # Product related queries
    if any(word in message_lower for word in ['product', 'item', 'buy', 'purchase', 'shop', 'what do you sell']):
        categories = db.session.query(Product.category).distinct().all()
        category_list = ', '.join([cat[0] for cat in categories])
        return f"We have 60+ products across categories: {category_list}.\n\nYou can:\n• Browse all products on the Products page\n• Search for specific items\n• Ask me to find products for you (e.g., 'Find me a laptop')\n• Get recommendations (e.g., 'Show me popular electronics')"
    
    # Category browsing
    categories_map = {
        'electronics': ['phone', 'laptop', 'mobile', 'computer', 'tv', 'headphone', 'watch', 'camera', 'speaker'],
        'clothing': ['shirt', 't-shirt', 'jacket', 'dress', 'shoes', 'suit', 'coat', 'sweater', 'fashion'],
        'home & garden': ['home', 'garden', 'kitchen', 'furniture', 'appliance', 'vacuum', 'purifier'],
        'beauty & health': ['beauty', 'skincare', 'makeup', 'health', 'fitness', 'massage', 'toothbrush'],
        'sports & outdoors': ['sports', 'outdoor', 'gym', 'yoga', 'bike', 'treadmill', 'camping', 'swimming'],
        'books & media': ['book', 'kindle', 'vinyl', 'guitar', 'drone', 'media', 'music'],
        'toys & games': ['toy', 'game', 'lego', 'puzzle', 'board game', 'play'],
        'automotive': ['car', 'auto', 'vehicle', 'dash cam', 'vacuum cleaner']
    }
    
    for category, keywords in categories_map.items():
        if any(keyword in message_lower for keyword in keywords):
            cat_products = Product.query.filter(Product.category.ilike(f'%{category}%')).filter_by(is_active=True).limit(3).all()
            if cat_products:
                result = f"Here are some popular {category} items:\n\n"
                for p in cat_products:
                    result += f"• {p.name} - ₹{int(p.price):,}\n"
                result += f"\nWe have {Product.query.filter(Product.category.ilike(f'%{category}%')).count()} products in {category}!"
                return result
    
    # Order tracking
    if any(word in message_lower for word in ['order', 'track', 'status', 'where is my order', 'my purchase']):
        if user:
            recent_orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).limit(3).all()
            if recent_orders:
                result = "Here are your recent orders:\n\n"
                for order in recent_orders:
                    result += f"📦 Order #{order.order_number}\n   Status: {order.order_status.title()}\n   Total: ₹{int(order.total_amount):,}\n\n"
                result += "Visit 'My Orders' for full details and tracking information!"
                return result
            else:
                return "You don't have any orders yet. Start shopping and your orders will appear here!"
        else:
            return "Please log in to track your orders. Once logged in, visit 'My Orders' in your profile menu to see all your order details!"
    
    # Shipping related
    if any(word in message_lower for word in ['shipping', 'delivery', 'shipping cost', 'when will it arrive', 'how long']):
        return "🚚 Shipping Options:\n• Standard: FREE (5-7 business days)\n• Express: ₹829 (2-3 business days)\n• Overnight: ₹1659 (Next day delivery)\n\nDelivery times vary by location. You can select your preferred method during checkout!"
    
    # Payment related
    if any(word in message_lower for word in ['payment', 'pay', 'card', 'cod', 'cash', 'upi', 'emi']):
        return "💳 Payment Methods:\n• Credit/Debit Cards (Visa, Mastercard, RuPay)\n• UPI (Google Pay, PhonePe, Paytm)\n• Net Banking (all major banks)\n• Cash on Delivery (COD)\n• EMI options available\n\nAll online payments are 100% secure with SSL encryption!"
    
    # Return/Refund
    if any(word in message_lower for word in ['return', 'refund', 'exchange', 'cancel', 'money back']):
        return "🔄 Return Policy:\n• 7-day hassle-free returns\n• Free pickup from your address\n• Full refund within 5-7 business days\n• Items must be unused with original packaging\n\nTo initiate a return, go to 'My Orders' and select the order you want to return."
    
    # Account related
    if any(word in message_lower for word in ['account', 'login', 'signup', 'register', 'password', 'sign up']):
        return "👤 Account Options:\n• New user? Click 'Sign Up' to create an account\n• Existing user? Click 'Login' to access your profile\n• Benefits: Order tracking, saved addresses, wishlist, exclusive offers\n\nYour account is secure with encrypted password protection!"
    
    # Cart related
    if any(word in message_lower for word in ['cart', 'add to cart', 'remove from cart', 'basket']):
        if user:
            cart_items = CartItem.query.filter_by(user_id=user.id).all()
            if cart_items:
                total = sum(item.product.price * item.quantity for item in cart_items)
                return f"🛒 You have {len(cart_items)} item(s) in your cart. Total: ₹{int(total):,}\n\nClick the cart icon to view details and proceed to checkout!"
            else:
                return "Your cart is empty. Browse products and click 'Add to Cart' to start shopping!"
        return "🛒 Cart Features:\n• Add items by clicking 'Add to Cart' on product pages\n• View cart by clicking the cart icon (top right)\n• Update quantities or remove items anytime\n• Save items for later\n\nYour cart is saved automatically when you login!"
    
    # Offers and deals
    if any(word in message_lower for word in ['offer', 'deal', 'sale', 'discount', 'promo', 'coupon']):
        return "🎉 Current Offers:\n• Free shipping on orders over ₹4,150\n• New users get 10% off first order\n• Seasonal sales on Electronics & Fashion\n• Bank offers: Extra 5% off with select credit cards\n\nCheck the homepage banner for limited-time deals!"
    
    # Comparison
    if any(word in message_lower for word in ['compare', 'difference', 'which is better', 'vs', 'versus']):
        return "To compare products, visit the product pages and check the specifications. You can also:\n• Read customer reviews\n• Compare ratings\n• Check feature lists\n• Look at price differences\n\nNeed help deciding? Tell me what you're looking for and I'll recommend the best option!"
    
    # Warranty
    if any(word in message_lower for word in ['warranty', 'guarantee', 'repair', 'service']):
        return "🛡️ Warranty Information:\n• All electronics come with 1-year manufacturer warranty\n• Extended warranty available at checkout\n• Free service for warranty claims\n• 24/7 customer support for technical issues\n\nCheck individual product pages for specific warranty details."
    
    # Gift related
    if any(word in message_lower for word in ['gift', 'present', 'wrap', 'occasion']):
        return "🎁 Gift Options:\n• Free gift wrapping available\n• Add a personalized message\n• Gift cards available (₹500 - ₹10,000)\n• Direct shipping to recipient's address\n\nSelect 'This is a gift' option during checkout!"
    
    # Help/Support
    if any(word in message_lower for word in ['help', 'support', 'contact', 'customer service', 'assistance', 'faq']):
        return "❓ How can I help you?\n• Type 'find [product]' to search products\n• Type 'recommend [category]' for suggestions\n• Ask about orders, shipping, payments\n• Or describe what you're looking for!\n\nFor human support: support@cartify.com | 1800-123-4567"
    
    # Time-related queries
    if any(word in message_lower for word in ['time', 'hour', 'open', 'close', 'working hours']):
        return "🕐 We're always open! Cartify is available 24/7 for online shopping. Customer support is available:\n• Phone: 9 AM - 9 PM (Mon-Sat)\n• Email: 24/7 response within 4 hours\n• Live Chat: 8 AM - 10 PM daily"
    
    # Complaints/Feedback
    if any(word in message_lower for word in ['complaint', 'feedback', 'review', 'bad', 'problem', 'issue']):
        return "We're sorry to hear you're facing issues. Please:\n• Email us at support@cartify.com\n• Call 1800-123-4567\n• Or use the Contact Us page\n\nWe value your feedback and will resolve your concern within 24 hours!"
    
    # Thank you
    if any(word in message_lower for word in ['thank', 'thanks', 'thankyou', 'appreciate']):
        responses = [
            "You're welcome! Happy shopping! 🛍️",
            "Glad I could help! Let me know if you need anything else! 😊",
            "My pleasure! Enjoy your shopping experience at Cartify! ✨",
            "Anytime! Have a wonderful day! 🌟"
        ]
        import random
        return random.choice(responses)
    
    # Goodbye
    if any(word in message_lower for word in ['bye', 'goodbye', 'see you', 'exit', 'quit']):
        return "Goodbye! Thanks for visiting Cartify. Come back soon for more amazing deals! Have a great day! 👋"
    
    # Jokes/Fun
    if any(word in message_lower for word in ['joke', 'funny', 'laugh', 'humor']):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
            "I told my wife she was drawing her eyebrows too high. She looked surprised! 🤨",
            "Why don't eggs tell jokes? They'd crack each other up! 🥚"
        ]
        import random
        return random.choice(jokes) + "\n\nNow, how can I help you with your shopping?"
    
    # Default response with suggestions
    suggestions = [
        "Try asking me:\n• 'Find me a laptop'\n• 'Show me popular products'\n• 'What are your shipping options?'\n• 'Track my order'",
        "I can help you with:\n• Product search\n• Price checks\n• Order tracking\n• Recommendations\n\nWhat would you like to know?",
        "I'm here to assist! You can say:\n• 'Find [product name]'\n• 'Recommend electronics'\n• 'Show me affordable items'\n• 'Help with my order'"
    ]
    import random
    return random.choice(suggestions)


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and return bot responses"""
    data = request.get_json()
    message = data.get('message', '').strip()
    session_id = data.get('session_id') or session.get('chat_session_id')
    
    if not session_id:
        session_id = str(uuid.uuid4())
        session['chat_session_id'] = session_id
    
    if not message:
        return jsonify({'success': False, 'error': 'Message is required'}), 400
    
    # Get current user if logged in
    user = None
    user_id = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user_id = user.id if user else None
    
    # Generate response
    response = get_chatbot_response(message, user)
    
    # Save chat message to database
    chat_msg = ChatMessage(
        user_id=user_id,
        session_id=session_id,
        message=message,
        response=response
    )
    db.session.add(chat_msg)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'response': response,
        'session_id': session_id,
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/chat/history')
def chat_history():
    """Get chat history for current session or user"""
    session_id = request.args.get('session_id') or session.get('chat_session_id')
    
    if not session_id and 'user_id' not in session:
        return jsonify({'success': True, 'messages': []})
    
    query = ChatMessage.query
    
    if 'user_id' in session:
        query = query.filter((ChatMessage.user_id == session['user_id']) | (ChatMessage.session_id == session_id))
    else:
        query = query.filter(ChatMessage.session_id == session_id)
    
    messages = query.order_by(ChatMessage.created_at.asc()).limit(50).all()
    
    return jsonify({
        'success': True,
        'messages': [msg.to_dict() for msg in messages]
    })


@app.route('/api/chat/clear', methods=['POST'])
def clear_chat():
    """Clear chat history for current session"""
    session_id = request.get_json().get('session_id') or session.get('chat_session_id')
    
    if session_id:
        ChatMessage.query.filter_by(session_id=session_id).delete()
        db.session.commit()
    
    return jsonify({'success': True, 'message': 'Chat history cleared'})


# Email Verification Routes
# OTP verification removed - Direct signup implemented

# OTP resend removed - Direct signup implemented

# OTP login removed intentionally.

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Send password reset email"""
    data = request.get_json()
    email = data.get('email', '').strip()
    
    if not email:
        return jsonify({'success': False, 'message': 'Email is required.'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        # Don't reveal if email exists or not for security
        return jsonify({'success': True, 'message': 'If an account with this email exists, a password reset link has been sent.'})
    
    try:
        send_password_reset_email(user)
        return jsonify({'success': True, 'message': 'Password reset email sent successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to send password reset email.'}), 500

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    try:
        user_id = User.verify_email_token(token)
        if not user_id:
            flash('Invalid or expired reset token.', 'error')
            return redirect(url_for('login'))
        
        user = User.query.get(user_id)
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            if not password or len(password) < 6:
                flash('Password must be at least 6 characters long.', 'error')
                return render_template('reset_password.html', token=token)
            
            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                return render_template('reset_password.html', token=token)
            
            user.set_password(password)
            db.session.commit()
            
            flash('Password reset successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        
        return render_template('reset_password.html', token=token)
        
    except Exception as e:
        flash('An error occurred during password reset.', 'error')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
