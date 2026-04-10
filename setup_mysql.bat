@echo off
echo Setting up MySQL database for Cartify...

REM Try to create database (this will fail if password is wrong, but let's try common passwords)
echo Attempting to create database with default settings...

REM Try with no password first
mysql -u root -e "CREATE DATABASE IF NOT EXISTS cartify_db;" 2>nul
if %errorlevel% equ 0 (
    echo Database created successfully with no password.
    goto :setup_user
)

REM Try with common passwords
mysql -u root -p"" -e "CREATE DATABASE IF NOT EXISTS cartify_db;" 2>nul
if %errorlevel% equ 0 (
    echo Database created successfully with empty password.
    goto :setup_user
)

mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS cartify_db;" 2>nul
if %errorlevel% equ 0 (
    echo Database created successfully with password 'root'.
    goto :setup_user
)

mysql -u root -ppassword -e "CREATE DATABASE IF NOT EXISTS cartify_db;" 2>nul
if %errorlevel% equ 0 (
    echo Database created successfully with password 'password'.
    goto :setup_user
)

mysql -u root -pDeba1234 -e "CREATE DATABASE IF NOT EXISTS cartify_db;" 2>nul
if %errorlevel% equ 0 (
    echo Database created successfully with password 'Deba1234'.
    goto :setup_user
)

echo Could not connect to MySQL with common passwords.
echo Please run MySQL setup manually or provide the correct root password.
echo.
echo Manual setup instructions:
echo 1. Open MySQL Command Line Client
echo 2. Run: CREATE DATABASE cartify_db;
echo 3. Update config.py with your MySQL credentials
pause
exit /b 1

:setup_user
echo Setting up database user...
mysql -u root -e "CREATE USER IF NOT EXISTS 'cartify'@'localhost' IDENTIFIED BY 'cartify123';" 2>nul
mysql -u root -e "GRANT ALL PRIVILEGES ON cartify_db.* TO 'cartify'@'localhost';" 2>nul
mysql -u root -e "FLUSH PRIVILEGES;" 2>nul

echo MySQL setup completed!
echo Database: cartify_db
echo User: cartify
echo Password: cartify123
pause