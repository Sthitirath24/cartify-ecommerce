from flask import current_app, render_template
from flask_mail import Mail, Message
import secrets
from datetime import datetime, timedelta
from models import db, User

mail = Mail()

def init_mail(app):
    """Initialize Flask-Mail with app"""
    mail.init_app(app)

def send_email_verification(user):
    """Send email verification link to user"""
    token = user.generate_email_verification_token()
    db.session.commit()

    verification_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:5000')}/verify-email/{token}"

    msg = Message(
        'Verify Your Cartify Account',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email]
    )

    msg.html = render_template('email/verify_email.html',
                             user=user,
                             verification_url=verification_url)

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def send_otp_email(email, otp_code):
    """Send OTP code for signup verification"""
    msg = Message(
        'Verify Your Cartify Account - OTP',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[email]
    )

    msg.html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #333; text-align: center;">Welcome to Cartify!</h2>
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3 style="color: #007bff; margin-top: 0;">Your OTP Code</h3>
            <div style="font-size: 32px; font-weight: bold; color: #28a745; text-align: center; margin: 20px 0; letter-spacing: 5px;">
                {otp_code}
            </div>
            <p style="margin: 10px 0; color: #666;">
                This code will expire in <strong>10 minutes</strong>.
            </p>
            <p style="margin: 10px 0; color: #666;">
                Enter this code on the signup verification page to complete your account creation.
            </p>
        </div>
        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
            <p style="color: #999; font-size: 12px;">
                If you didn't request this signup, please ignore this email.
            </p>
            <p style="color: #999; font-size: 12px;">
                © 2024 Cartify. All rights reserved.
            </p>
        </div>
    </div>
    """

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"OTP email sending failed: {e}")
        return False
        return True
    except Exception as e:
        print(f"OTP email sending failed: {e}")
        return False

def send_password_reset_email(user):
    """Send password reset email"""
    token = secrets.token_urlsafe(32)
    user.email_verification_token = token
    user.email_verification_expires = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()

    reset_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:5000')}/reset-password/{token}"

    msg = Message(
        'Reset Your Cartify Password',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email]
    )

    msg.html = render_template('email/reset_password.html',
                             user=user,
                             reset_url=reset_url)

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Password reset email sending failed: {e}")
        return False

def send_order_confirmation_email(order):
    """Send order confirmation email"""
    msg = Message(
        f'Order Confirmation - #{order.order_number}',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[order.user.email]
    )

    msg.html = render_template('email/order_confirmation.html',
                             order=order,
                             user=order.user)

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Order confirmation email sending failed: {e}")
        return False

def send_welcome_email(user):
    """Send welcome email to new user"""
    msg = Message(
        'Welcome to Cartify!',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email]
    )

    msg.html = render_template('email/welcome.html', user=user)

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Welcome email sending failed: {e}")
        return False