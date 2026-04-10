from functools import wraps
from flask import session, redirect, url_for, flash, request, jsonify
from models import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Please log in first'}), 401
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Please log in first'}), 401
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Admin access required'}), 403
            flash('Admin access required.', 'error')
            return redirect(url_for('home'))
        
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get the current logged-in user"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

def login_user(user):
    """Log in a user"""
    session['user_id'] = user.id
    session['username'] = user.username
    session['is_admin'] = user.is_admin
    session.permanent = True

def logout_user():
    """Log out the current user"""
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_admin', None)

