#!/usr/bin/env python3
"""
Email verification helper for development testing
"""

import pymysql
import sys

def verify_all_emails():
    """Mark all user emails as verified"""
    try:
        conn = pymysql.connect(
            host='localhost',
            user='cartify',
            password='cartify123',
            database='cartify_db',
            port=3306
        )
        cursor = conn.cursor()

        # Update all unverified emails to verified
        cursor.execute("UPDATE user SET email_verified = 1 WHERE email_verified = 0")

        affected_rows = cursor.rowcount
        conn.commit()

        print(f"✅ Verified {affected_rows} email(s)")

        # Show current users
        cursor.execute("SELECT username, email, email_verified FROM user")
        users = cursor.fetchall()

        print("\n📧 Current users:")
        print("-" * 50)
        for user in users:
            status = "✅ Verified" if user[2] else "❌ Unverified"
            print(f"Username: {user[0]}")
            print(f"Email: {user[1]}")
            print(f"Status: {status}")
            print("-" * 30)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def show_verification_tokens():
    """Show verification tokens for manual verification"""
    try:
        conn = pymysql.connect(
            host='localhost',
            user='cartify',
            password='cartify123',
            database='cartify_db',
            port=3306
        )
        cursor = conn.cursor()

        cursor.execute("SELECT username, email, email_verification_token FROM user WHERE email_verification_token IS NOT NULL")
        tokens = cursor.fetchall()

        if tokens:
            print("\n🔗 Verification Links (for manual testing):")
            print("-" * 60)
            for token in tokens:
                link = f"http://localhost:5000/verify-email/{token[2]}"
                print(f"User: {token[0]} ({token[1]})")
                print(f"Link: {link}")
                print("-" * 40)
        else:
            print("No pending verification tokens found.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("📧 Cartify Email Verification Helper")
    print("=" * 40)

    if len(sys.argv) > 1 and sys.argv[1] == "--tokens":
        show_verification_tokens()
    else:
        verify_all_emails()
        print("\n💡 Tip: All users can now login without email verification!")
        print("   Run with --tokens to see verification links if needed.")

if __name__ == "__main__":
    main()