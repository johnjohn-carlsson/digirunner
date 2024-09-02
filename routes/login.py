from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from database import User  # Assuming your User model is in a file named models.py
from flask_login import login_user, current_user, logout_user

loginBluePrint = Blueprint('login', __name__)

@loginBluePrint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))  # Redirect to home if user is already logged in
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Fetch the user by username or email
        user:User = User.query.filter((User.Username == username) | (User.Email == username)).first()

        if user and check_password_hash(user.Password, password):
            login_user(user)
            return redirect(url_for('index.index'))  # Redirect to home page or a dashboard
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@loginBluePrint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))