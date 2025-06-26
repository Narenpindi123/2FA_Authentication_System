from flask import Flask, render_template, request, redirect, session, url_for, flash
import pyotp
import qrcode
import io
import os
import bcrypt
from base64 import b64encode

app = Flask(__name__)
app.secret_key = os.urandom(24)

users = {}

@app.route('/')
def index():
    if session.get('username'):
        return render_template('dashboard.html', user=session['username'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required')
            return redirect(url_for('register'))

        if username in users:
            flash('Username already exists')
            return redirect(url_for('register'))

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        secret = pyotp.random_base32()
        users[username] = {'password': hashed, '2fa_secret': secret}

        session['username'] = username
        session['2fa_secret'] = secret
        return redirect(url_for('setup_2fa'))

    return render_template('register.html')

@app.route('/setup-2fa')
def setup_2fa():
    username = session.get('username')
    secret = session.get('2fa_secret')

    if not username or not secret:
        flash('You must register first.')
        return redirect(url_for('register'))

    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=username, issuer_name="SecureApp")

    img = qrcode.make(uri)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_code = b64encode(buffer.getvalue()).decode()

    return render_template('setup_2fa.html', qr_code=qr_code)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required')
            return redirect(url_for('login'))

        user = users.get(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['temp_user'] = username
            return redirect(url_for('verify_2fa'))

        flash('Invalid username or password')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    username = session.get('temp_user')
    if not username:
        flash('Session expired. Please login again.')
        return redirect(url_for('login'))

    user = users.get(username)
    if not user:
        flash('User not found')
        return redirect(url_for('login'))

    if request.method == 'POST':
        token = request.form.get('token')
        if not token:
            flash('Token is required')
            return redirect(url_for('verify_2fa'))

        totp = pyotp.TOTP(user['2fa_secret'])
        if totp.verify(token):
            session.pop('temp_user', None)
            session['username'] = username
            return redirect(url_for('index'))

        flash('Invalid 2FA token')
        return redirect(url_for('verify_2fa'))

    return render_template('verify_2fa.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
