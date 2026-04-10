#!/usr/bin/env python3
"""
Manual MySQL Setup for Cartify
Run this after you've set your MySQL root password
"""

import pymysql
import sys
import getpass

def create_database_with_password(root_password):
    """Create database using provided root password"""
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
    print("🔧 Manual MySQL Setup for Cartify")
    print("=" * 35)

    print("\nEnter your MySQL root password to create the database:")
    root_password = getpass.getpass("MySQL Root Password: ")

    if create_database_with_password(root_password):
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python init_db.py")
        print("2. Run: python app.py")
        print("\nThe app will use MySQL database: cartify_db")
        print("User: cartify, Password: cartify123")
    else:
        print("\n❌ Setup failed. Please check your root password and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()