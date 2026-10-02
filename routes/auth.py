# Authentication Routes for 9-Table Database Architecture
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.authentication_service import AuthenticationService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username_or_email = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        user = AuthenticationService.authenticate_user(username_or_email, password)
        if user:
            session['user_id'] = user.user_id
            session['name'] = user.name
            session['username'] = user.username
            session['email'] = user.email
            session['role'] = user.role
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('index'))
        
        flash('Invalid username/email or password. Please try again.', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registers a new user into USERS table."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'member')
        
        if not name:
            name = username

        success, msg = AuthenticationService.register_user(name, username, email, password, role)
        if success:
            flash('Registration successful! Please log in with your credentials.', 'success')
            return redirect(url_for('auth.login'))
        flash(msg, 'danger')
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    """Logs out user and clears session."""
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
def profile():
    """Renders profile of currently logged-in user."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user_info = AuthenticationService.get_user_by_id(session['user_id'])
    return render_template('auth/profile.html', user=user_info)

@auth_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """Updates password for authenticated user."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        old_pwd = request.form.get('old_password')
        new_pwd = request.form.get('new_password')
        success, msg = AuthenticationService.change_password(session['user_id'], old_pwd, new_pwd)
        if success:
            flash(msg, 'success')
            return redirect(url_for('auth.profile'))
        flash(msg, 'danger')
    return render_template('auth/change_password.html')
