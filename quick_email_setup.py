#!/usr/bin/env python3
"""
Quick Email Setup for Cartify OTP
"""

import os

def setup_email():
    """Quick setup for Gmail app password"""
    print("🔧 Quick Gmail App Password Setup for Cartify")
    print("=" * 50)
    print()

    print("📧 To send OTP emails, you need a Gmail App Password:")
    print("   1. Go to: https://myaccount.google.com/apppasswords")
    print("   2. Sign in with: zoomy@2006@gmail.com")
    print("   3. Select 'Mail' and 'Windows Computer' (or your device)")
    print("   4. Click 'Generate' and copy the 16-character password")
    print()

    app_password = input("Enter your 16-character Gmail App Password: ").strip().replace(' ', '')

    if len(app_password) != 16:
        print("❌ Error: App password must be exactly 16 characters!")
        print("   Make sure you copied it correctly (no spaces)")
        return False

    # Update .env file
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()

        # Replace the placeholder
        content = content.replace('MAIL_PASSWORD=your_gmail_app_password_here', f'MAIL_PASSWORD={app_password}')

        with open(env_file, 'w') as f:
            f.write(content)

        print("✅ Email configuration updated successfully!")
        print(f"   📧 From: zoomy@2006@gmail.com")
        print(f"   🔑 App Password: {'*' * 12} (configured)")
        print()
        print("🚀 Ready to test OTP signup!")
        print("   Run: python app.py")
        print("   Visit: http://localhost:5000/signup")
        return True
    else:
        print("❌ Error: .env file not found!")
        return False

if __name__ == "__main__":
    setup_email()