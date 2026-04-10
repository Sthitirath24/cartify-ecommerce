#!/usr/bin/env python3
"""
Test signup and login functionality
"""

import requests
import random
from app import app, User

def test_signup_login():
    """Test signup and login"""
    
    # Test 1: Login with existing user
    print("=" * 60)
    print("TEST 1: Login with existing user (admin@cartify.com)")
    print("=" * 60)
    try:
        session = requests.Session()
        r = session.post('http://localhost:5000/login', 
                        data={'email': 'admin@cartify.com', 'password': 'admin'},
                        timeout=5,
                        allow_redirects=False)
        if r.status_code in [200, 302]:
            print(f'✅ Login request successful: {r.status_code}')
            if r.status_code == 302:
                print(f'   Redirected to: {r.headers.get("Location", "home")}')
        else:
            print(f'❌ Login failed: {r.status_code}')
    except Exception as e:
        print(f'❌ Error: {e}')

    # Test 2: Create new user  
    print()
    print("=" * 60)
    print("TEST 2: Register new user")
    print("=" * 60)
    rand_id = random.randint(10000, 99999)
    try:
        data = {
            'username': f'testuser{rand_id}',
            'email': f'testuser{rand_id}@example.com',
            'password': 'TestPass@123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        print(f"Registering: {data['email']}")
        r = requests.post('http://localhost:5000/signup', data=data, timeout=5, allow_redirects=False)
        print(f'✅ Signup response: {r.status_code}')
        if r.status_code == 302:
            print(f'   Redirected to: {r.headers.get("Location", "login")}')
    except Exception as e:
        print(f'❌ Error: {e}')
        return

    # Test 3: Verify new user in database
    print()
    print("=" * 60)
    print("TEST 3: Verify new user in database")
    print("=" * 60)
    try:
        with app.app_context():
            email = f'testuser{rand_id}@example.com'
            user = User.query.filter_by(email=email).first()
            if user:
                print(f'✅ User found in database')
                print(f'   Username: {user.username}')
                print(f'   Email: {user.email}')
                print(f'   Password works: {user.check_password("TestPass@123")}')
                print(f'   Welcome points: {user.loyalty_points.total_points if user.loyalty_points else 0}')
            else:
                print(f'❌ User not found in database')
    except Exception as e:
        print(f'❌ Error: {e}')

    # Test 4: Try to login with new user
    print()
    print("=" * 60)
    print("TEST 4: Login with newly created user")
    print("=" * 60)
    try:
        session = requests.Session()
        email = f'testuser{rand_id}@example.com'
        r = session.post('http://localhost:5000/login', 
                        data={'email': email, 'password': 'TestPass@123'},
                        timeout=5,
                        allow_redirects=False)
        if r.status_code in [200, 302]:
            print(f'✅ Login successful: {r.status_code}')
            if r.status_code == 302:
                print(f'   Redirected to: {r.headers.get("Location", "home")}')
        else:
            print(f'❌ Login failed: {r.status_code}')
    except Exception as e:
        print(f'❌ Error: {e}')

    print()
    print("=" * 60)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    test_signup_login()
