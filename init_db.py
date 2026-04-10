#!/usr/bin/env python3
"""
Database initialization script for Cartify
This script creates all database tables and optionally populates with sample data
"""

from app import app, db
from models import User, Product, Order, OrderItem, CartItem, Review, ChatMessage, LoyaltyPoints, LoyaltyTransaction
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_tables():
    """Create all database tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Tables created successfully!")

def populate_sample_data():
    """Populate database with sample data"""
    with app.app_context():
        print("Populating sample data...")

        # Create admin user
        admin = User(
            username='admin',
            email='admin@cartify.com',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Create sample products
        products_data = [
            {
                'name': 'iPhone 15 Pro Max',
                'price': 149999.0,
                'category': 'Electronics',
                'description': 'Latest iPhone with A17 Pro chip, titanium design, and advanced camera system.',
                'stock_quantity': 50,
                'image_url': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400',
                'rating': 4.8,
                'review_count': 1247
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'price': 129999.0,
                'category': 'Electronics',
                'description': 'Premium Android flagship with S Pen, 200MP camera, and AI features.',
                'stock_quantity': 30,
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400',
                'rating': 4.7,
                'review_count': 892
            },
            {
                'name': 'MacBook Pro 16"',
                'price': 249999.0,
                'category': 'Electronics',
                'description': 'Powerful laptop with M3 Max chip, 16GB RAM, and stunning Liquid Retina XDR display.',
                'stock_quantity': 20,
                'image_url': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400',
                'rating': 4.9,
                'review_count': 567
            },
            {
                'name': 'Sony WH-1000XM5',
                'price': 29999.0,
                'category': 'Electronics',
                'description': 'Industry-leading noise canceling wireless headphones with 30-hour battery life.',
                'stock_quantity': 100,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
                'rating': 4.6,
                'review_count': 2156
            },
            {
                'name': 'Nike Air Max 270',
                'price': 12999.0,
                'category': 'Fashion',
                'description': 'Comfortable running shoes with visible Air unit in heel for superior cushioning.',
                'stock_quantity': 75,
                'image_url': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400',
                'rating': 4.4,
                'review_count': 892
            },
            {
                'name': 'Levi\'s 501 Original',
                'price': 8999.0,
                'category': 'Fashion',
                'description': 'Classic straight fit jeans made with premium denim, perfect for any occasion.',
                'stock_quantity': 60,
                'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
                'rating': 4.3,
                'review_count': 1243
            }
        ]

        for product_data in products_data:
            product = Product(**product_data)
            db.session.add(product)

        # Create sample user
        user = User(
            username='demo',
            email='demo@example.com',
            first_name='Demo',
            last_name='User'
        )
        user.set_password('demo123')
        db.session.add(user)

        db.session.commit()
        print("Sample data populated successfully!")

if __name__ == '__main__':
    create_tables()
    populate_sample_data()
    print("Database initialization completed!")