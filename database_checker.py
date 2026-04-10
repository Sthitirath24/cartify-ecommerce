#!/usr/bin/env python3
"""
Database and Product Checker
Checks database presence, total products, and fixes missing images
"""

import os
import sqlite3
from app import app
from models import db, Product

def check_database_presence():
    """Check if database is present and identify it"""
    print("=== Database Presence Check ===")
    
    # Check different possible database locations
    possible_db_paths = [
        'instance/cartify_dev.db',
        'instance/cartify.db',
        'cartify.db',
        'data/cartify.db',
        'database/cartify.db'
    ]
    
    db_found = False
    active_db_path = None
    
    for db_path in possible_db_paths:
        if os.path.exists(db_path):
            print(f"✅ Database found at: {db_path}")
            db_found = True
            active_db_path = db_path
            
            # Get database info
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print(f"   Tables: {[table[0] for table in tables]}")
                
                cursor.execute("SELECT COUNT(*) FROM product")
                product_count = cursor.fetchone()[0]
                print(f"   Products in DB: {product_count}")
                
                cursor.execute("SELECT COUNT(*) FROM user")
                user_count = cursor.fetchone()[0]
                print(f"   Users in DB: {user_count}")
                
                conn.close()
            except Exception as e:
                print(f"   Error reading database: {e}")
    
    if not db_found:
        print("❌ No database found in expected locations")
        print("\nHow to identify database:")
        print("1. Look for .db files in project directory")
        print("2. Check app.py for DATABASE_URL configuration")
        print("3. Check instance/ folder for SQLite database")
        print("4. Use Flask's app.config['SQLALCHEMY_DATABASE_URI']")
    
    return db_found, active_db_path

def check_and_fix_blank_images():
    """Check for products with blank/missing images and fix them"""
    with app.app_context():
        print("\n=== Checking for Blank Images ===")
        
        # Get all products
        products = Product.query.all()
        total_products = len(products)
        
        print(f"Total products to check: {total_products}")
        
        blank_images = []
        fixed_count = 0
        
        # Default images for different categories
        default_images = {
            'Electronics': 'https://images.unsplash.com/photo-1498049794561-77b7b21085ab?w=400',
            'Clothing': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
            'Home & Garden': 'https://images.unsplash.com/photo-1589894061455-1123441d78d2?w=400',
            'Beauty & Health': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400',
            'Sports & Outdoors': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400',
            'Books & Media': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
            'Toys & Games': 'https://images.unsplash.com/photo-1581833971358-2c8b550bdc4a?w=400',
            'Automotive': 'https://images.unsplash.com/photo-1542362567-b07e54358753?w=400',
            'Food & Beverages': 'https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=400'
        }
        
        for product in products:
            needs_fix = False
            
            # Check for blank or None image
            if not product.image_url or product.image_url.strip() == '':
                blank_images.append(product.id)
                needs_fix = True
                
                # Assign default image based on category
                if product.category in default_images:
                    product.image_url = default_images[product.category]
                else:
                    product.image_url = default_images['Electronics']  # Fallback
                
                fixed_count += 1
                print(f"Fixed blank image for: {product.name} (ID: {product.id})")
        
        # Save changes
        if fixed_count > 0:
            try:
                db.session.commit()
                print(f"✅ Fixed {fixed_count} products with blank images")
            except Exception as e:
                print(f"❌ Error fixing images: {e}")
                db.session.rollback()
        else:
            print("✅ All products have images")
        
        return blank_images, fixed_count

def update_product_count_display():
    """Update product count in templates"""
    print("\n=== Updating Product Count Display ===")
    
    # Check if products.html template shows total count
    template_path = 'templates/products.html'
    
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if total_products display is present
        if 'total_products' in content:
            print("✅ Template already shows total product count")
        else:
            print("⚠️  Template needs update for product count display")
    
    with app.app_context():
        total_products = Product.query.filter_by(is_active=True).count()
        print(f"Current total active products: {total_products}")
        
        # Get count by category
        categories = db.session.query(Product.category).distinct().all()
        print("\nProduct count by category:")
        for category in sorted(categories):
            count = Product.query.filter_by(category=category[0]).count()
            print(f"  {category[0]}: {count}")

def create_database_info_file():
    """Create a file with database information"""
    with app.app_context():
        db_info = {
            'total_products': Product.query.count(),
            'active_products': Product.query.filter_by(is_active=True).count(),
            'categories': [cat[0] for cat in db.session.query(Product.category).distinct().all()],
            'database_path': app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured'),
            'last_updated': str(Product.query.order_by(Product.updated_at.desc()).first().updated_at) if Product.query.first() else 'No products'
        }
        
        with open('database_info.txt', 'w') as f:
            f.write("=== Cartify Database Information ===\n\n")
            f.write(f"Total Products: {db_info['total_products']}\n")
            f.write(f"Active Products: {db_info['active_products']}\n")
            f.write(f"Database Path: {db_info['database_path']}\n")
            f.write(f"Last Updated: {db_info['last_updated']}\n\n")
            f.write("Categories:\n")
            for category in sorted(db_info['categories']):
                count = Product.query.filter_by(category=category).count()
                f.write(f"  {category}: {count} products\n")
        
        print("✅ Database information saved to database_info.txt")

def main():
    """Main function to run all checks"""
    print("=== Cartify Database and Product Checker ===")
    
    # Check database presence
    db_found, db_path = check_database_presence()
    
    if db_found:
        # Check and fix blank images
        blank_images, fixed_count = check_and_fix_blank_images()
        
        # Update product count display
        update_product_count_display()
        
        # Create database info file
        create_database_info_file()
        
        print("\n=== Summary ===")
        print(f"Database: {'Found' if db_found else 'Not Found'}")
        print(f"Blank Images Fixed: {fixed_count}")
        print(f"Total Products: {Product.query.count()}")
    else:
        print("\n❌ Please set up the database first")
        print("Run: python init_db.py")

if __name__ == "__main__":
    main()
