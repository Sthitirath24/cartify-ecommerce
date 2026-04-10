#!/usr/bin/env python3
"""
Initialize SQLite database with sample data
"""

from app import app, db
from models import Product, User
from werkzeug.security import generate_password_hash

def init_sample_data():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()

        print("Adding sample users...")
        # Create admin user
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
            print("✓ Admin user created")

        # Create demo user
        demo = User.query.filter_by(email='demo@example.com').first()
        if not demo:
            demo = User(
                username='demo',
                email='demo@example.com',
                first_name='Demo',
                last_name='User'
            )
            demo.set_password('demo123')
            db.session.add(demo)
            print("✓ Demo user created")

        print("Adding sample products...")
        # Add sample products
        products = [
            {
                'name': 'iPhone 15 Pro Max',
                'price': 149999.0,
                'category': 'Electronics',
                'stock_quantity': 50,
                'image_url': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400',
                'rating': 4.8,
                'review_count': 1247
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'price': 129999.0,
                'category': 'Electronics',
                'stock_quantity': 30,
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400',
                'rating': 4.7,
                'review_count': 892
            },
            {
                'name': 'MacBook Pro 16"',
                'price': 249999.0,
                'category': 'Electronics',
                'stock_quantity': 20,
                'image_url': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400',
                'rating': 4.9,
                'review_count': 567
            },
            {
                'name': 'Sony WH-1000XM5',
                'price': 29999.0,
                'category': 'Electronics',
                'stock_quantity': 100,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
                'rating': 4.6,
                'review_count': 2156
            },
            {
                'name': 'Nike Air Max 270',
                'price': 12999.0,
                'category': 'Fashion',
                'stock_quantity': 75,
                'image_url': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400',
                'rating': 4.4,
                'review_count': 892
            },
            {
                'name': 'Levi\'s 501 Original',
                'price': 8999.0,
                'category': 'Fashion',
                'stock_quantity': 60,
                'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
                'rating': 4.3,
                'review_count': 1243
            }
        ]

        for p in products:
            if not Product.query.filter_by(name=p['name']).first():
                product = Product(**p)
                db.session.add(product)

        db.session.commit()
        print(f"✓ Added {len(products)} sample products")

        print("\n🎉 Database initialization completed!")
        print("\n📋 Login Credentials:")
        print("Admin: admin / admin123")
        print("Demo User: demo / demo123")
        print("\n🌐 Visit: http://localhost:5000")

if __name__ == "__main__":
    init_sample_data()