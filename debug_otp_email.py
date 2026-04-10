#!/usr/bin/env python3
"""
Test OTP Email Sending - Debug Version
"""

import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from config import Config
from email_service import init_mail, send_otp_email
import pyotp

def test_otp_email_with_debug():
    """Test email sending with detailed debug information"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    init_mail(app)
    
    with app.app_context():
        print("=" * 60)
        print("🔍 OTP EMAIL CONFIGURATION DEBUG")
        print("=" * 60)
        
        # Check configuration
        print(f"📧 MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
        print(f"🔓 MAIL_PORT: {app.config.get('MAIL_PORT')}")
        print(f"🔐 MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
        print(f"👤 MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
        password = app.config.get('MAIL_PASSWORD')
        print(f"🔑 MAIL_PASSWORD length: {len(password) if password else 0}")
        print(f"🔑 MAIL_PASSWORD first 4 chars: {password[:4] if password else 'None'}***")
        
        if not password:
            print("❌ ERROR: MAIL_PASSWORD is not set!")
            return False
        
        if len(password) != 16:
            print(f"❌ ERROR: MAIL_PASSWORD should be 16 chars, got {len(password)}")
            return False
        
        print("\n✅ Configuration looks good!")
        print("\n" + "=" * 60)
        print("📧 TESTING EMAIL SENDING")
        print("=" * 60)
        
        # Get test email
        test_email = input("\n📧 Enter your email address to test: ").strip()
        
        if not test_email:
            print("❌ No email provided")
            return False
        
        # Generate OTP
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        otp_code = totp.now()
        
        print(f"\n🔢 Generated OTP Code: {otp_code}")
        print(f"📨 Sending to: {test_email}")
        print("\n⏳ Attempting to send email...")
        
        try:
            result = send_otp_email(test_email, otp_code)
            if result:
                print("✅ EMAIL SENT SUCCESSFULLY!")
                print(f"   From: {app.config.get('MAIL_USERNAME')}")
                print(f"   To: {test_email}")
                print(f"   OTP: {otp_code}")
                print("\n✅ Check your inbox (and spam folder) for the OTP email!")
                return True
            else:
                print("❌ Email sending returned False")
                return False
        except Exception as e:
            print(f"❌ EXCEPTION OCCURRED: {e}")
            print(f"   Exception type: {type(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = test_otp_email_with_debug()
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST PASSED - Emails are sending correctly!")
    else:
        print("❌ TEST FAILED - Check configuration and error messages above")
    print("=" * 60)
