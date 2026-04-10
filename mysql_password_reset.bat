@echo off
echo MySQL Root Password Reset Guide for Cartify
echo ===========================================
echo.
echo Since automated setup failed, please reset your MySQL root password:
echo.
echo Step 1: Stop MySQL Service (run as Administrator)
echo Right-click Command Prompt ^> Run as Administrator
echo net stop mysql80
echo.
echo Step 2: Start MySQL in Safe Mode (run as Administrator)
echo "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe" --skip-grant-tables --user=mysql
echo.
echo Step 3: Open new Command Prompt (as Administrator) and connect:
echo "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root
echo.
echo Step 4: In MySQL prompt, reset password:
echo USE mysql;
echo UPDATE user SET authentication_string=PASSWORD('new_password') WHERE User='root';
echo FLUSH PRIVILEGES;
echo EXIT;
echo.
echo Step 5: Stop MySQL (Ctrl+C in the safe mode window)
echo.
echo Step 6: Start MySQL Service normally
echo net start mysql80
echo.
echo Step 7: Test connection with new password
echo "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
echo (enter your new password)
echo.
echo After resetting, run: python simple_mysql_setup.py
echo.
pause</content>
<parameter name="filePath">d:\zooma\Cartify 1\Cartify\mysql_password_reset.bat