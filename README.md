# 🔐 Two-Factor Authentication (2FA) System

This project implements a secure login system that combines traditional password-based authentication with Time-based One-Time Passwords (TOTP), providing an extra layer of protection for user accounts.

## 🛠️ Features

- User registration and login
- Passwords hashed with bcrypt
- TOTP-based 2FA using Google Authenticator or Authy
- QR code generation for easy 2FA setup
- Session management with Flask
- Basic HTML frontend with Bootstrap styling

## 🧱 Tech Stack

- Python (Flask)
- SQLite (lightweight database)
- `PyOTP` for TOTP generation/validation
- `qrcode` for QR code rendering
- `bcrypt` for secure password hashing
- HTML/CSS (Bootstrap)

## 🚀 How It Works

1. **User Registers**: Enters email and password (stored securely).
2. **2FA Setup**: A TOTP secret is generated and displayed as a QR code.
3. **User Scans QR**: Using Google Authenticator, the user adds the key.
4. **Login Process**:
   - Step 1: Enter email/password
   - Step 2: Enter the current 6-digit 2FA code from their app
5. **Verification**: The TOTP is validated using the shared secret.

## 🧪 Security Considerations

- Passwords are salted and hashed using `bcrypt`
- TOTP ensures dynamic codes every 30 seconds
- Prevents common attacks like credential stuffing, phishing, or session hijacking

## 🖥️ Screenshots

<h2>📸 Screenshots</h2>

<table>
  <tr>
    <td><strong>Login</strong></td>
    <td><strong>Register</strong></td>
  </tr>
  <tr>
    <td><img src="Screenshots/Login.png" width="300"></td>
    <td><img src="Screenshots/Register.png" width="300"></td>
  </tr>
  <tr>
    <td><strong>QR Code Setup</strong></td>
    <td><strong>2FA Token Entry</strong></td>
  </tr>
  <tr>
    <td><img src="Screenshots/QR.png" width="300"></td>
    <td><img src="Screenshots/Wrong2FA.png" width="300"></td>
  </tr>
  <tr>
    <td><strong>Successful Login</strong></td>
    <td><strong>Duo Mobile Linked</strong></td>
  </tr>
  <tr>
    <td><img src="Screenshots/Welcome.png" width="300"></td>
    <td><img src="Screenshots/2fa.jng" width="300"></td>
  </tr>
</table>
