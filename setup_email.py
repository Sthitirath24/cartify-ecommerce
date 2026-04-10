#!/usr/bin/env python3
"""
Email Configuration Setup for Cartify
"""

import os
import getpass

def setup_email_config():
    """Set up email configuration for sending OTPs"""
    print("🔧 Cartify Email Configuration Setup")
    print("=" * 40)
    print()

    print("📧 To send OTP emails, we need your Gmail App Password.")
    print("   (NOT your regular Gmail password)")
    print()

    print("📋 How to get your Gmail App Password:")
    print("   1. Go to https://myaccount.google.com/security")
    print("   2. Enable 2-Factor Authentication if not already enabled")
    print("   3. Go to 'App passwords' section")
    print("   4. Generate a new app password for 'Cartify'")
    print("   5. Copy the 16-character password (ignore spaces)")
    print()

    app_password = getpass.getpass("Enter your Gmail App Password: ")

    if not app_password or len(app_password.replace(' ', '')) != 16:
        print("❌ Invalid app password format. It should be 16 characters.")
        return False

    # Set environment variable
    os.environ['MAIL_PASSWORD'] = app_password.replace(' ', '')

    print("✅ Email configuration updated!")
    print(f"   📧 From: zoomy@2006@gmail.com")
    print(f"   🔑 App Password: {'*' * 12} (set)")
    print()
    print("🚀 You can now test the signup with OTP!")
    print("   Visit: http://localhost:5000/signup")

    return True

if __name__ == "__main__":
    setup_email_config()