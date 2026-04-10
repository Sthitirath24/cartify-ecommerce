# MySQL Setup Guide for Cartify

## Prerequisites
- MySQL Server 8.0 is installed and running
- Python environment is set up with requirements.txt installed

## Step 1: Reset MySQL Root Password (if needed)

If you don't know your MySQL root password or the automated setup failed:

1. Run the password reset batch file as Administrator:
   ```
   mysql_password_reset.bat
   ```

2. Follow the on-screen instructions to reset your MySQL root password.

## Step 2: Manual Database Setup

After setting your root password:

1. Run the manual setup script:
   ```
   python manual_mysql_setup.py
   ```

2. Enter your MySQL root password when prompted.

3. The script will create:
   - Database: `cartify_db`
   - User: `cartify` with password `cartify123`

## Step 3: Initialize Database

1. Create database tables:
   ```
   python init_db.py
   ```

2. (Optional) Add sample data:
   ```
   python init_sample_data.py
   ```

## Step 4: Run the Application

```
python app.py
```

## Alternative: Using MySQL Workbench

If you prefer using MySQL Workbench:

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Create a new schema named `cartify_db`
4. Create a new user `cartify@localhost` with password `cartify123`
5. Grant all privileges on `cartify_db.*` to the user
6. Then proceed with Step 3 above

## Configuration

The application is now configured to use MySQL by default:
- Database: `cartify_db`
- User: `cartify`
- Password: `cartify123`
- Host: `localhost`
- Port: `3306`

## Troubleshooting

- **Connection failed**: Ensure MySQL service is running
- **Access denied**: Check that the `cartify` user has proper permissions
- **Database not found**: Run `python init_db.py` to create tables

## Database Commands

To explore your MySQL database:

```bash
# Connect to MySQL as cartify user
mysql -u cartify -p cartify_db
# Password: cartify123

# Show all tables
SHOW TABLES;

# View users
SELECT * FROM user LIMIT 10;

# View products
SELECT * FROM product LIMIT 10;

# View orders
SELECT * FROM order LIMIT 10;
```