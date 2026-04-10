#!/bin/bash

# 🚀 Cartify GitHub Deployment Script
# This script helps you deploy Cartify to GitHub and Render

echo "🛍️  Cartify Deployment Script"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Git is initialized
if [ ! -d ".git" ]; then
    print_info "Initializing Git repository..."
    git init
    print_status "Git repository initialized"
else
    print_status "Git repository already exists"
fi

# Add all files to Git
print_info "Adding all files to Git..."
git add .

# Check for changes
if git diff --cached --quiet; then
    print_warning "No changes to commit"
else
    # Commit changes
    print_info "Committing changes..."
    git commit -m "$(date '+%Y-%m-%d %H:%M:%S') - Production ready deployment with enhanced chatbot and trending features"
    print_status "Changes committed successfully"
fi

# Check if remote origin exists
if git remote get-url origin &>/dev/null; then
    print_status "Remote origin already exists"
    print_info "Pushing to GitHub..."
    git push origin main
    print_status "Code pushed to GitHub successfully"
else
    print_error "No remote origin found!"
    echo "Please set up your GitHub repository first:"
    echo "1. Go to https://github.com"
    echo "2. Create a new repository named 'cartify-ecommerce'"
    echo "3. Run: git remote add origin https://github.com/YOUR_USERNAME/cartify-ecommerce.git"
    echo "4. Run this script again"
    exit 1
fi

# Check if Render configuration exists
if [ -f "render.yaml" ]; then
    print_status "Render configuration found"
else
    print_warning "render.yaml not found - creating basic configuration..."
    cat > render.yaml << EOF
services:
  - type: web
    name: cartify-web
    env: python
    plan: starter
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn --bind 0.0.0.0:\$PORT app:app"
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: cartify-db
          property: connectionString
    autoDeploy: true
    healthCheckPath: /health

  - type: pserv
    name: cartify-db
    plan: starter
    databaseName: cartify
    user: cartify_user
EOF
    print_status "Basic render.yaml created"
fi

# Check if Procfile exists
if [ -f "Procfile" ]; then
    print_status "Procfile found"
else
    print_warning "Procfile not found - creating..."
    echo "web: gunicorn --bind 0.0.0.0:\$PORT app:app" > Procfile
    print_status "Procfile created"
fi

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    print_status "requirements.txt found"
else
    print_error "requirements.txt not found!"
    echo "Please ensure requirements.txt exists with all dependencies"
    exit 1
fi

echo ""
echo "🌐 Next Steps for Render Deployment:"
echo "=================================="
echo "1. Go to https://render.com"
echo "2. Click 'New +' → 'Web Service'"
echo "3. Connect your GitHub repository"
echo "4. Configure environment variables:"
echo "   - FLASK_ENV=production"
echo "   - SECRET_KEY=your-secret-key"
echo "   - DATABASE_URL=your-postgres-connection-string"
echo "   - MAIL_SERVER=smtp.gmail.com"
echo "   - MAIL_PORT=587"
echo "   - MAIL_USE_TLS=true"
echo "5. Add PostgreSQL database service"
echo "6. Deploy! Your app will be available at: https://your-app.onrender.com"

echo ""
print_status "Deployment script completed successfully!"
echo "Your Cartify e-commerce platform is ready for production deployment! 🎉"
