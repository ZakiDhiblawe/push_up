from flask import Blueprint, flash, render_template, url_for,request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from . models import User 
from . import db
from flask_login import  login_user, logout_user, login_required

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
    



#logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))