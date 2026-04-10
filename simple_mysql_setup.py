#!/usr/bin/env python3
"""
Simple MySQL Setup for Cartify
"""

import pymysql
import sys

def test_mysql_connection():
    """Test MySQL connection with different credentials"""
    credentials = [
        {'user': 'root', 'password': '', 'host': 'localhost', 'port': 3306},
        {'user': 'root', 'password': 'root', 'host': 'localhost', 'port': 3306},
        {'user': 'root', 'password': 'password', 'host': 'localhost', 'port': 3306},
        {'user': 'root', 'password': '123456', 'host': 'localhost', 'port': 3306},
        {'user': 'root', 'password': 'admin', 'host': 'localhost', 'port': 3306},
        {'user': 'root', 'password': 'Deba1234', 'host': 'localhost', 'port': 3306},
    ]

    for cred in credentials:
        try:
            conn = pymysql.connect(**cred)
            print(f"✅ Connected successfully with user: {cred['user']}, password: '{cred['password']}'")
            conn.close()
            return cred
        except Exception as e:
            print(f"❌ Failed with user: {cred['user']}, password: '{cred['password']}' - {str(e)}")
            continue

    return None

def create_database(credentials):
    """Create the cartify_db database"""
    try:
        conn = pymysql.connect(**credentials)
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS cartify_db")
        print("✅ Database 'cartify_db' created successfully!")

        cursor.execute("CREATE USER IF NOT EXISTS 'cartify'@'localhost' IDENTIFIED BY 'cartify123'")
        cursor.execute("GRANT ALL PRIVILEGES ON cartify_db.* TO 'cartify'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")
        print("✅ User 'cartify' created with password 'cartify123'")

        conn.commit()
        cursor.close()
        conn.close()

        return True
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def update_config():
    """Update config.py to use MySQL"""
    config_content = '''class MySQLDevelopmentConfig(Config):
    """Development configuration using MySQL database"""
    DEBUG = True
    # Format: mysql+pymysql://username:password@host:port/database_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://cartify:cartify123@localhost:3306/cartify_db'
'''

    try:
        with open('config.py', 'r') as f:
            content = f.read()

        # Find and replace the MySQL config
        start = content.find('class MySQLDevelopmentConfig(Config):')
        if start != -1:
            end = content.find('class ProductionConfig(Config):', start)
            if end == -1:
                end = len(content)

            old_config = content[start:end]
            new_content = content.replace(old_config, config_content)

            with open('config.py', 'w') as f:
                f.write(new_content)

            print("✅ Updated config.py to use MySQL")
            return True
    except Exception as e:
        print(f"❌ Error updating config.py: {e}")
        return False

def main():
    print("🚀 Simple MySQL Setup for Cartify")
    print("=" * 40)

    # Test connection
    print("\n1. Testing MySQL connections...")
    working_credentials = test_mysql_connection()

    if not working_credentials:
        print("\n❌ Could not connect to MySQL with any credentials.")
        print("\n🔧 Please ensure MySQL is running and try one of these:")
        print("   - Reset MySQL root password")
        print("   - Use MySQL Workbench to create database manually")
        print("   - Check MySQL service status")
        sys.exit(1)

    # Create database and user
    print("\n2. Creating database and user...")
    if not create_database(working_credentials):
        sys.exit(1)

    # Update config
    print("\n3. Updating configuration...")
    if not update_config():
        sys.exit(1)

    print("\n🎉 MySQL setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Set environment variable: set FLASK_ENV=mysql_development")
    print("2. Run: python app.py")
    print("3. The app will create tables and migrate data automatically")

if __name__ == "__main__":
    main()