# Cartify - Modern E-commerce Website

Cartify is a comprehensive, modern e-commerce website built with Flask, Bootstrap, and SQLAlchemy (supports both SQLite and MySQL). It features a beautiful, responsive design with enhanced user experience and all the essential e-commerce functionality.

## Features

### Core E-commerce Features
- **Product Management**: Dynamic product catalog with categories, pricing, and inventory
- **Shopping Cart**: Persistent cart with real-time updates
- **Order Processing**: Complete order lifecycle with status tracking
- **User Authentication**: Secure login, registration, and profile management
- **Payment Integration**: Multiple payment methods (Cards, UPI, Net Banking, COD)

### 🤖 AI-Powered Chatbot
- **Multilingual Support**: English, Hindi, Odia, Tamil, Telugu
- **Real-World Scenarios**: Product search, order tracking, cart management
- **Smart Recommendations**: AI-powered product suggestions
- **Context Awareness**: Remembers user preferences and conversation history

### 📊 Advanced Features
- **Trending Products**: AI-powered trending algorithm with real-time updates
- **Product Recommendations**: Personalized suggestions based on browsing history
- **Review System**: Customer ratings and feedback
- **Wishlist Management**: Save favorite products for later
- **Loyalty Points**: Reward system for repeat customers

### 🎨 Modern UI/UX
- **Responsive Design**: Mobile-first approach
- **Interactive Elements**: Smooth animations and micro-interactions
- **Real-time Updates**: Live cart count, notifications
- **Accessibility**: WCAG compliant design

## 🚀 Features

### Core E-commerce Features
- **Product Catalog**: Browse products by category with search and filtering
- **Product Details**: Detailed product pages with images, descriptions, and reviews
- **Shopping Cart**: Add, remove, and update items with real-time cart management
- **User Authentication**: Secure login/signup system with session management
- **Checkout Process**: Complete checkout with shipping and payment information
- **Order Management**: View order history and track order status
- **Inventory Management**: Real-time stock tracking and low stock alerts
- **Admin Panel**: Product management, order processing, and user administration

### User Experience Features
- **Responsive Design**: Mobile-first design that works on all devices
- **Modern UI/UX**: Beautiful gradient designs, smooth animations, and intuitive navigation
- **Real-time Updates**: Live cart updates and dynamic content loading
- **Interactive Elements**: Hover effects, loading states, and user feedback
- **Search & Filter**: Advanced product search and category filtering

### Technical Features
- **Flask Backend**: Robust Python web framework
- **Database Support**: SQLite (default) or MySQL for production
- **SQLAlchemy ORM**: Object-relational mapping for database operations
- **Bootstrap 5**: Modern CSS framework for responsive design
- **Font Awesome**: Professional icons throughout the interface
- **JavaScript**: Interactive functionality and AJAX requests
- **Session Management**: Secure user sessions and cart persistence

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (development) / MySQL (production)
- **ORM**: SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript
- **CSS Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Inter)

## 📦 Quick Start (SQLite - Recommended for Beginners)

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Cartify
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```
   Or use the provided batch file:
   ```bash
   run.bat
   ```

6. **Access the Application**
   - Open your browser and go to: `http://localhost:5000`
   - Admin login: username: `admin`, password: `admin123`
   - Demo user: username: `demo`, password: `demo123`

## 🐬 MySQL Setup (For Production)

### Prerequisites
- Python 3.7 or higher
- MySQL Server 8.0 or higher
- pip (Python package installer)

### MySQL Database Setup

#### Option 1: Interactive Setup (Recommended)
1. **Run the MySQL setup batch file**:
   ```bash
   mysql_setup.bat
   ```
   This will prompt you for your MySQL root password and set up everything automatically.

#### Option 2: Manual Setup
1. **Open MySQL Command Line Client** or MySQL Workbench
2. **Create database and user**:
   ```sql
   -- Connect as root user
   CREATE DATABASE cartify_db;
   CREATE USER 'cartify'@'localhost' IDENTIFIED BY 'cartify123';
   GRANT ALL PRIVILEGES ON cartify_db.* TO 'cartify'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. **Update Database Configuration**:
   - Open `config.py`
   - The `MySQLDevelopmentConfig` is already configured to use:
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://cartify:cartify123@localhost:3306/cartify_db'
   ```

4. **Set environment variable**:
   ```bash
   set FLASK_ENV=mysql_development
   ```

5. **Initialize database**:
   ```bash
   python init_db.py
   ```

### Troubleshooting MySQL Setup

If you encounter connection issues:

1. **Check MySQL service**:
   ```bash
   # Windows
   Get-Service MYSQL80

   # Or check Services.msc
   ```

2. **Test MySQL connection**:
   ```bash
   mysql -u root -p -e "SELECT VERSION();"
   ```

3. **Reset MySQL root password** (if needed):
   - Stop MySQL service
   - Start MySQL in safe mode: `mysqld --skip-grant-tables`
   - Reset password in another terminal
   - Restart MySQL normally

4. **Firewall issues**: Ensure MySQL port 3306 is not blocked

## 🔧 Configuration

### Environment Variables
You can configure the application using environment variables:

- `FLASK_ENV`: Set to `development` (SQLite) or `mysql_development` (MySQL)
- `SECRET_KEY`: Application secret key (auto-generated if not set)
- `DATABASE_URL`: Override database connection URL

### Database Migration
If you need to update the database schema:
1. Stop the application
2. Update your models in `models.py`
3. Run the initialization script again:
   ```bash
   python init_db.py
   ```

## 📊 Database Features

### SQLite (Development)
- **File-based**: Single file database, easy to backup
- **Zero configuration**: No server setup required
- **Fast setup**: Ready to run immediately
- **Perfect for development**: Quick prototyping and testing

### MySQL (Production)
- **Persistent Data Storage**: All user data persists across restarts
- **Concurrent Users**: Multiple users can shop simultaneously
- **Advanced Queries**: Complex filtering, sorting, and search
- **Data Analytics**: Order history, user behavior tracking
- **Scalability**: Ready for production deployment
- **Backup & Recovery**: Enterprise-grade reliability

## 🛒 Usage

### For Customers
1. Browse products on the homepage
2. Use search and filters to find specific items
3. Add products to cart
4. Register/Login to checkout
5. Complete order with shipping information
6. Track orders in profile section

### For Administrators
1. Login with admin credentials
2. Access admin panel to manage products
3. View and process orders
4. Monitor inventory levels
5. Add new products and categories

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

### SQLite Issues
- Ensure virtual environment is activated
- Check that all dependencies are installed
- Verify Python version compatibility

### MySQL Issues
- Verify MySQL server is running
- Check database credentials in `config.py`
- Ensure user has proper permissions
- Test connection manually with MySQL client

For additional help, please check the console output for error messages and refer to the troubleshooting sections above.

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the website**
   Open your browser and go to `http://localhost:5000`

## 🎯 Usage Guide

### For Customers

1. **Browse Products**
   - Visit the home page to see featured products
   - Use the navigation menu to browse by category
   - Use the search bar to find specific products

2. **Product Details**
   - Click on any product to view detailed information
   - See product images, descriptions, specifications, and reviews
   - Add products to cart or wishlist

3. **Shopping Cart**
   - Add products to your cart from any product page
   - View cart contents and update quantities
   - Remove items or continue shopping

4. **Checkout Process**
   - Review cart items and proceed to checkout
   - Fill in shipping and payment information
   - Complete your purchase securely

5. **Account Management**
   - Create an account or sign in
   - View order history and manage profile
   - Update personal information and preferences

### For Developers

The application follows a clean, modular structure:

```
Cartify/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── home.html         # Home page
│   ├── products.html     # Product catalog
│   ├── product_detail.html # Product details
│   ├── cart.html         # Shopping cart
│   ├── checkout.html     # Checkout process
│   ├── login.html        # User login
│   ├── signup.html       # User registration
│   └── profile.html      # User profile
└── static/               # Static assets (CSS, JS, images)
```

## 🎨 Design Features

### Color Scheme
- **Primary**: Indigo (#6366f1)
- **Secondary**: Purple (#8b5cf6)
- **Accent**: Amber (#f59e0b)
- **Success**: Green (#10b981)
- **Danger**: Red (#ef4444)

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700
- **Responsive**: Scales appropriately on all devices

### Components
- **Cards**: Modern card designs with hover effects
- **Buttons**: Gradient buttons with smooth transitions
- **Forms**: Clean, accessible form designs
- **Navigation**: Responsive navigation with dropdown menus
- **Alerts**: Beautiful notification system

## 🔧 Customization

### Adding New Products
Edit the `products` list in `app.py`:

```python
products = [
    {
        'id': 7,
        'name': 'New Product Name',
        'price': 99.99,
        'category': 'Electronics',
        'image': 'product.jpg',
        'description': 'Product description here.',
        'rating': 4.5,
        'reviews': 50,
        'in_stock': True
    }
]
```

### Modifying Styles
- Edit the CSS in `templates/base.html`
- Update color variables in the `:root` selector
- Modify component styles as needed

### Adding New Features
- Create new routes in `app.py`
- Add corresponding templates in `templates/`
- Update navigation in `base.html`

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
For production deployment, consider:

1. **Use a production WSGI server** (Gunicorn, uWSGI)
2. **Set up a proper database** (PostgreSQL, MySQL)
3. **Configure environment variables**
4. **Set up HTTPS/SSL**
5. **Use a reverse proxy** (Nginx, Apache)

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 📱 Responsive Design

The website is fully responsive and optimized for:
- **Desktop**: Full-featured experience
- **Tablet**: Optimized layout for medium screens
- **Mobile**: Touch-friendly interface

## 🔒 Security Features

- **Session Management**: Secure user sessions
- **Form Validation**: Client and server-side validation
- **CSRF Protection**: Built-in Flask security
- **Input Sanitization**: Safe handling of user input

## 🎯 Future Enhancements

- [ ] Database integration (SQLAlchemy)
- [ ] Payment gateway integration (Stripe, PayPal)
- [ ] Email notifications
- [ ] Admin panel
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Advanced search filters
- [ ] Multi-language support
- [ ] Dark mode theme
- [ ] Mobile app

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created with ❤️ for modern e-commerce experiences.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

---

**Cartify** - Your Ultimate Shopping Destination 🛒✨
=======
# cartify-ecommerce
>>>>>>> ba0a52caec706c2aab9e0efe7930314614dba73f
