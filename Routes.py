from flask import render_template, request, redirect, session, flash
from app import app
from models import db, User, ShortLink
from datetime import timedelta
import secrets

def generate_short_code():
    return secrets.token_urlsafe(5)

@app.route('/')
def home():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('dashboard.html', user=user)
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        session['user_id'] = user.id
        flash('Login successful!', 'success')
    else:
        flash('Invalid credentials. Please try again.', 'error')

    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect('/')

@app.route('/create_link', methods=['POST'])
def create_link():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect('/')

    user = User.query.get(session['user_id'])
    original_url = request.form.get('original_url')

    if not original_url:
        flash('Please provide a valid URL.', 'error')
        return redirect('/')

    short_code = generate_short_code()
    expiration_date = datetime.utcnow() + timedelta(hours=48)

    new_link = ShortLink(original_url=original_url, short_code=short_code, user=user, expiration_date=expiration_date)
    db.session.add(new_link)
    db.session.commit()

    flash(f'Short link created: {request.host_url}{short_code}', 'success')
    return redirect('/')

@app.route('/analytics')
def analytics():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect('/')

    user = User.query.get(session['user_id'])
    user_links = ShortLink.query.filter_by(user=user).all()

    return render_template('analytics.html', user=user, user_links=user_links)
