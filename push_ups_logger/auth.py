from flask import Blueprint, flash, render_template, url_for,request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from . models import User 
from . import db
from flask_login import  login_user, logout_user, login_required
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message
from . import db, mail
from .models import User
import secrets
import os

auth = Blueprint('auth', __name__)



#loging page
@auth.route('/login')
def login():
    return render_template('home/login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Invalid credentials, please try again.', 'danger')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))



#singup page
@auth.route('/signup')
def signup():
    return render_template('home/register.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Check if passwords match
    if password != confirm_password:
        flash('Passwords do not match.', 'danger')
        return redirect(url_for('auth.signup'))

    # Validate password strength
    import re
    strong_password = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
    if not strong_password.match(password):
        flash('Password must be at least 8 characters long, include one uppercase letter, one lowercase letter, and one symbol.', 'danger')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email already registered. Please log in.', 'warning')
        return redirect(url_for('auth.signup'))
    
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()
    
    flash('Registration successful! Please log in.', 'success')
    return redirect(url_for('auth.login'))
    

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = secrets.token_urlsafe(20)
            user.reset_token = token
            db.session.commit()

            reset_link = url_for('auth.reset_password', token=token, _external=True)
            msg = Message('Password Reset Request',
                  sender='Maarta17@@gmail.com',
                  recipients=[user.email])
            msg.body = f'''To reset your password, visit the following link:
            {reset_link}
 
            If you did not make this request, simply ignore this email and no changes will be made.
            '''
            mail.send(msg)

            flash('A password reset link has been sent to your email.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email not found.', 'danger')
    return render_template('home/forgot_password.html')


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first_or_404()
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('Passwords do not match.', 'danger')
        else:
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
            user.reset_token = None
            db.session.commit()
            flash('Your password has been updated. You can now log in with your new password.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('home/reset_password.html', token=token)



#logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))