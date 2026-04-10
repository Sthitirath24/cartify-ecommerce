#!/usr/bin/env python3
"""
Create a test user for authentication testing
"""

from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def create_test_user():
    """Create a test user for login testing"""
    with app.app_context():
        # Check if test user already exists
        existing_user = User.query.filter_by(email='test@example.com').first()
        if existing_user:
            print("Test user already exists!")
            return

        # Create test user
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            email_verified=True  # Skip email verification for testing
        )
        user.set_password('password123')

        try:
            db.session.add(user)
            db.session.commit()
            print("✅ Test user created successfully!")
            print("Email: test@example.com")
            print("Password: password123")
            print("Username: testuser")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating test user: {e}")

if __name__ == "__main__":
    create_test_user()