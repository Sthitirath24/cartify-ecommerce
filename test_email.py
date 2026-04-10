#!/usr/bin/env python3
"""
Test Email Sending for Cartify OTP
"""

from flask import Flask
from config import Config
from email_service import init_mail, send_otp_email
import pyotp

def test_email():
    """Test email sending functionality"""
    app = Flask(__name__)
    app.config.from_object(Config)

    init_mail(app)

    with app.app_context():
        # Generate a test OTP
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        otp_code = totp.now()

        test_email = input("Enter your email address to test OTP sending: ").strip()

        if not test_email:
            print("❌ No email provided!")
            return

        print(f"📧 Sending test OTP to: {test_email}")
        print(f"🔢 OTP Code: {otp_code}")

        success = send_otp_email(test_email, otp_code)

        if success:
            print("✅ Email sent successfully!")
            print("   Check your inbox (and spam folder) for the OTP email.")
        else:
            print("❌ Email sending failed!")
            print("   Check your Gmail app password configuration.")

if __name__ == "__main__":
    test_email()