#!/usr/bin/env python3
"""
Set up Gmail App Password for Cartify OTP
"""

import os

def setup_gmail_app_password():
    print("🔧 Setting up Gmail App Password for Cartify")
    print("=" * 50)
    print()

    print("📧 Your Gmail account: sthitiprakalpitarath@gmail.com")
    print("🔑 You need a Gmail App Password (NOT your regular password)")
    print()

    print("📋 Steps to get your App Password:")
    print("   1. Go to: https://myaccount.google.com/apppasswords")
    print("   2. Sign in with: sthitiprakalpitarath@gmail.com")
    print("   3. Select 'Mail' and 'Other (custom name)'")
    print("   4. Enter 'Cartify' as the custom name")
    print("   5. Click 'Generate'")
    print("   6. Copy the 16-character password (ignore spaces)")
    print()

    app_password = input("Enter your 16-character Gmail App Password: ").strip().replace(' ', '')

    if len(app_password) != 16:
        print("❌ Error: App password must be exactly 16 characters!")
        print("   Make sure you copied it correctly from Google.")
        return False

    # Update .env file
    env_path = '.env'
    try:
        with open(env_path, 'r') as f:
            content = f.read()

        # Replace the placeholder
        old_line = 'MAIL_PASSWORD=REPLACE_WITH_YOUR_16_CHAR_GMAIL_APP_PASSWORD'
        new_line = f'MAIL_PASSWORD={app_password}'
        content = content.replace(old_line, new_line)

        with open(env_path, 'w') as f:
            f.write(content)

        print("✅ SUCCESS: Gmail App Password configured!")
        print(f"   📧 From: sthitiprakalpitarath@gmail.com")
        print(f"   🔑 App Password: {'*' * 12} (configured)")
        print()
        print("🚀 Ready to send OTP emails to any email address!")
        print("   Run: python app.py")
        print("   Test signup at: http://localhost:5000/signup")
        return True

    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

if __name__ == "__main__":
    setup_gmail_app_password()