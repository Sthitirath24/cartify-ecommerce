@echo off
echo ========================================
echo    Cartify MySQL Setup Script
echo ========================================
echo.

echo This script will help you set up MySQL for Cartify.
echo Make sure MySQL 8.0 is installed and running.
echo.

set /p mysql_password="Enter your MySQL root password: "

echo.
echo Testing MySQL connection...
mysql -u root -p%mysql_password% -e "SELECT 1;" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Cannot connect to MySQL. Please check your password and MySQL service.
    pause
    exit /b 1
)

echo ✅ MySQL connection successful!
echo.

echo Creating database and user...
mysql -u root -p%mysql_password% -e "
CREATE DATABASE IF NOT EXISTS cartify_db;
CREATE USER IF NOT EXISTS 'cartify'@'localhost' IDENTIFIED BY 'cartify123';
GRANT ALL PRIVILEGES ON cartify_db.* TO 'cartify'@'localhost';
FLUSH PRIVILEGES;
"

if %errorlevel% neq 0 (
    echo ❌ Error creating database/user.
    pause
    exit /b 1
)

echo ✅ Database and user created successfully!
echo.
echo User: cartify
echo Password: cartify123
echo Database: cartify_db
echo.
echo To use MySQL, run:
echo set FLASK_ENV=mysql_development
echo python app.py
echo.
pause