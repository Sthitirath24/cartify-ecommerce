# 🚀 Cartify Deployment Guide

## 📋 Prerequisites
- GitHub account
- Render account (Free tier available)
- Cartify project ready for deployment

---

## 🛠️ Step 1: Prepare Your Project

### 1.1 Update Configuration Files
Make sure these files are in your project root:

#### `render.yaml` (Already created)
```yaml
services:
  - type: web
    name: cartify-web
    env: python
    plan: starter
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn --bind 0.0.0.0:$PORT app:app"
    envVars:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: cartify-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: MAIL_SERVER
        value: smtp.gmail.com
      - key: MAIL_PORT
        value: 587
      - key: MAIL_USE_TLS
        value: true
      - key: UPLOAD_FOLDER
        value: /app/uploads
    autoDeploy: true
    healthCheckPath: /health

  - type: pserv
    name: cartify-db
    plan: starter
    databaseName: cartify
    user: cartify_user
```

#### `Procfile` (Already created)
```
web: gunicorn --bind 0.0.0.0:$PORT app:app
```

#### `requirements.txt` (Already updated)
Contains all necessary dependencies including:
- Flask and extensions
- PostgreSQL driver (psycopg2-binary)
- Gunicorn (production server)
- All other required packages

#### `.gitignore` (Already created)
Excludes unnecessary files from Git repository.

### 1.2 Add Health Check Endpoint
Add this to your `app.py`:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

---

## 🐙 Step 2: Set Up GitHub Repository

### 2.1 Initialize Git
```bash
git init
git add .
git commit -m "Initial commit: Cartify e-commerce platform"
```

### 2.2 Create GitHub Repository
1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name: `cartify-ecommerce`
4. Description: `Modern e-commerce platform with Flask`
5. Make it Public
6. Don't initialize with README (we have one)
7. Click "Create repository"

### 2.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/cartify-ecommerce.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 3: Deploy to Render

### 3.1 Create Render Account
1. Go to [Render](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repositories

### 3.2 Create New Web Service
1. Click "New +" → "Web Service"
2. Select "Build and deploy from a Git repository"
3. Choose your `cartify-ecommerce` repository
4. Configure deployment:
   - **Name**: `cartify-web`
   - **Environment**: `Python 3`
   - **Branch**: `main`
   - **Root Directory**: `.` (leave empty)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Instance Type**: `Free` (or `Starter` for better performance)

### 3.3 Add Environment Variables
In Render Dashboard → your service → Environment:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
UPLOAD_FOLDER=/app/uploads
```

### 3.4 Add PostgreSQL Database
1. In Render Dashboard, click "New +" → "PostgreSQL"
2. **Name**: `cartify-db`
3. **Database Name**: `cartify`
4. **User**: `cartify_user`
5. **Plan**: `Free` (or `Starter`)
6. Click "Create Database"

### 3.5 Connect Database to Web Service
1. Go to your web service settings
2. Add environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Click "Connect" → select your `cartify-db`
3. Render will automatically populate the connection string

---

## 🔧 Step 4: Configure Production Settings

### 4.1 Update Database Configuration
In your `config.py`, ensure PostgreSQL is used in production:
```python
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # PostgreSQL will be automatically used by DATABASE_URL
```

### 4.2 Update App Configuration
In `app.py`, ensure production environment is used:
```python
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])
```

---

## 🚀 Step 5: Deploy and Test

### 5.1 Trigger Deployment
1. Push changes to GitHub:
```bash
git add .
git commit -m "Ready for production deployment"
git push origin main
```

2. Render will automatically detect changes and deploy

### 5.2 Monitor Deployment
- Check Render dashboard for build logs
- Wait for deployment to complete (usually 2-5 minutes)
- Your app will be available at: `https://cartify-web.onrender.com`

### 5.3 Test Your Application
1. Visit your Render URL
2. Test:
   - Homepage loads correctly
   - Product browsing works
   - User registration/login
   - Cart functionality
   - Checkout process

---

## 🛠️ Step 6: Post-Deployment Setup

### 6.1 Initialize Database
Add database initialization to your app startup:
```python
@app.before_first_request
def create_tables():
    db.create_all()
```

Or run manually via Render shell:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 6.2 Set Up Email Configuration
Update email settings in Render environment:
```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### 6.3 Configure Custom Domain (Optional)
1. In Render dashboard → your service → Custom Domains
2. Add your domain name
3. Update DNS records as instructed by Render

---

## 🔍 Step 7: Troubleshooting

### Common Issues and Solutions

#### **Build Fails**
- Check `requirements.txt` for correct versions
- Ensure all files are committed to Git
- Check Render build logs

#### **Database Connection Errors**
- Verify `DATABASE_URL` environment variable
- Check PostgreSQL service is running
- Ensure database name matches

#### **Application Not Loading**
- Check `startCommand` in Render configuration
- Verify Flask app entry point
- Check application logs

#### **Static Files Not Loading**
- Ensure `static` folder is in project root
- Check file permissions
- Verify URL generation in templates

#### **Email Not Working**
- Verify email environment variables
- Check if app passwords are used (not regular passwords)
- Ensure TLS is enabled

---

## 📊 Step 8: Monitor and Scale

### Monitoring
- Use Render dashboard for:
  - CPU usage
  - Memory usage
  - Response times
  - Error rates

### Scaling
- Upgrade from Free to Starter plan for:
  - Better performance
  - More RAM
  - Custom domains
  - SSL certificates

---

## 🎯 Quick Deployment Commands

```bash
# 1. Commit all changes
git add .
git commit -m "Production ready deployment"

# 2. Push to GitHub
git push origin main

# 3. Monitor deployment on Render dashboard
# URL: https://dashboard.render.com

# 4. Test application
# URL: https://your-app-name.onrender.com
```

---

## 📞 Support Resources

- **Render Documentation**: https://render.com/docs
- **Render Status**: https://status.render.com
- **GitHub Actions**: https://github.com/features/actions
- **Flask Deployment**: https://flask.palletsprojects.com/en/2.3.x/deploying/

---

## ✅ Deployment Checklist

- [ ] All configuration files created (`render.yaml`, `Procfile`, `requirements.txt`)
- [ ] `.gitignore` properly configured
- [ ] Health check endpoint added
- [ ] Database configuration updated for production
- [ ] Environment variables set in Render
- [ ] PostgreSQL database created and connected
- [ ] Application deployed successfully
- [ ] All major features tested
- [ ] Email configuration verified
- [ ] Custom domain configured (if needed)

---

🎉 **Your Cartify e-commerce platform is now live on Render!**

For any issues, check the Render dashboard logs and ensure all environment variables are correctly configured.
