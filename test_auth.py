#!/usr/bin/env python3
"""
Test authentication functionality
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

def test_signup():
    """Test user signup"""
    print("🧪 Testing user signup...")

    data = {
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': 'password123',
        'first_name': 'Test',
        'last_name': 'User2'
    }

    try:
        response = requests.post(f'{BASE_URL}/signup', data=data, allow_redirects=False)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 302:  # Redirect after successful signup
            print("✅ Signup successful! Redirected to login page.")
            return True
        else:
            print(f"❌ Signup failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error during signup: {e}")
        return False

def test_login():
    """Test user login"""
    print("\n🧪 Testing user login...")

    data = {
        'email': 'test@example.com',
        'password': 'password123'
    }

    try:
        response = requests.post(f'{BASE_URL}/login', data=data, allow_redirects=False)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 302:  # Redirect after successful login
            print("✅ Login successful! Redirected to home page.")
            return True
        else:
            print(f"❌ Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error during login: {e}")
        return False

def test_home_page():
    """Test accessing home page"""
    print("\n🧪 Testing home page access...")

    try:
        response = requests.get(f'{BASE_URL}/')
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            print("✅ Home page accessible!")
            return True
        else:
            print(f"❌ Home page error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing home page: {e}")
        return False

def main():
    print("🚀 Testing Cartify Authentication")
    print("=" * 40)

    # Test home page first
    if not test_home_page():
        print("❌ Cannot access home page. Is the app running?")
        return

    # Test signup
    test_signup()

    # Test login with existing user
    if test_login():
        print("\n🎉 All authentication tests passed!")
    else:
        print("\n❌ Login test failed!")

if __name__ == "__main__":
    main()