#!/usr/bin/env python3
"""
MySQL Setup for Cartify with provided password
"""

import pymysql
import sys

def create_database():
    """Create database using the provided root password"""
    root_password = "zoomy@2006"

    try:
        # Connect as root
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password=root_password,
            port=3306
        )
        cursor = conn.cursor()

        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS cartify_db")
        print("✅ Database 'cartify_db' created successfully!")

        # Create user
        cursor.execute("CREATE USER IF NOT EXISTS 'cartify'@'localhost' IDENTIFIED BY 'cartify123'")
        cursor.execute("GRANT ALL PRIVILEGES ON cartify_db.* TO 'cartify'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")
        print("✅ User 'cartify' created with password 'cartify123'")

        conn.commit()
        cursor.close()
        conn.close()

        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🔧 Setting up MySQL database for Cartify")
    print("=" * 40)

    if create_database():
        print("\n🎉 MySQL setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python init_db.py")
        print("2. Run: python app.py")
        print("\nThe app will use MySQL database: cartify_db")
        print("User: cartify, Password: cartify123")
    else:
        print("\n❌ Setup failed. Please check your MySQL installation and password.")
        sys.exit(1)

if __name__ == "__main__":
    main()