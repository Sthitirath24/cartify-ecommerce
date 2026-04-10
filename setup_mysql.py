#!/usr/bin/env python3
"""
MySQL Setup Script for Cartify
This script helps set up MySQL database and user for the Cartify application
"""

import subprocess
import sys
import os

def run_mysql_command(command, password=None):
    """Run a MySQL command and return success status"""
    try:
        if password:
            cmd = f'mysql -u root -p{password} -e "{command}"'
        else:
            cmd = f'mysql -u root -e "{command}"'

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_mysql_connection(password=None):
    """Test MySQL connection with given password"""
    success, stdout, stderr = run_mysql_command("SELECT VERSION();", password)
    return success

def create_database_and_user(password=None):
    """Create database and user"""
    commands = [
        "CREATE DATABASE IF NOT EXISTS cartify_db;",
        "CREATE USER IF NOT EXISTS 'cartify'@'localhost' IDENTIFIED BY 'cartify123';",
        "GRANT ALL PRIVILEGES ON cartify_db.* TO 'cartify'@'localhost';",
        "FLUSH PRIVILEGES;"
    ]

    for cmd in commands:
        success, stdout, stderr = run_mysql_command(cmd, password)
        if not success:
            print(f"Failed to execute: {cmd}")
            print(f"Error: {stderr}")
            return False

    return True

def main():
    print("Cartify MySQL Setup Script")
    print("=" * 30)

    # Test different password scenarios
    passwords_to_try = [None, "", "root", "password", "123456", "admin", "Deba1234"]

    working_password = None

    print("Testing MySQL connections...")
    for pwd in passwords_to_try:
        pwd_display = f"'{pwd}'" if pwd else "no password"
        print(f"Trying password: {pwd_display}", end="... ")

        if test_mysql_connection(pwd):
            print("SUCCESS!")
            working_password = pwd
            break
        else:
            print("FAILED")

    if working_password is None:
        print("\n❌ Could not connect to MySQL with any common passwords.")
        print("\n🔧 Manual MySQL Setup Required:")
        print("1. Open MySQL Command Line Client or MySQL Workbench")
        print("2. Create database: CREATE DATABASE cartify_db;")
        print("3. Create user: CREATE USER 'cartify'@'localhost' IDENTIFIED BY 'cartify123';")
        print("4. Grant permissions: GRANT ALL PRIVILEGES ON cartify_db.* TO 'cartify'@'localhost';")
        print("5. Flush privileges: FLUSH PRIVILEGES;")
        print("6. Update config.py with your MySQL root password")
        print("\nThen run: python init_db.py")
        return False

    print(f"\n✅ MySQL connection successful with password: {'(empty)' if working_password == '' else working_password}")

    # Create database and user
    print("\nCreating database and user...")
    if create_database_and_user(working_password):
        print("✅ Database and user created successfully!")
        print("Database: cartify_db")
        print("User: cartify")
        print("Password: cartify123")

        # Update config.py
        config_path = os.path.join(os.path.dirname(__file__), 'config.py')
        try:
            with open(config_path, 'r') as f:
                content = f.read()

            # Replace the MySQL config
            old_config = '''class MySQLDevelopmentConfig(Config):
    """Development configuration using MySQL database"""
    DEBUG = True
    # Format: mysql+pymysql://username:password@host:port/database_name
    # Using root user with no password (for development)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://root:@localhost:3306/cartify_db' '''

            new_config = '''class MySQLDevelopmentConfig(Config):
    """Development configuration using MySQL database"""
    DEBUG = True
    # Format: mysql+pymysql://username:password@host:port/database_name
    # Using the cartify user created by setup script
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://cartify:cartify123@localhost:3306/cartify_db' '''

            content = content.replace(old_config, new_config)

            with open(config_path, 'w') as f:
                f.write(content)

            print("✅ Updated config.py with MySQL credentials")

        except Exception as e:
            print(f"❌ Failed to update config.py: {e}")

        print("\n🚀 Next steps:")
        print("1. Change FLASK_ENV to 'mysql_development' in your environment")
        print("2. Run: python init_db.py")
        print("3. Run: python app.py")

        return True
    else:
        print("❌ Failed to create database and user")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)