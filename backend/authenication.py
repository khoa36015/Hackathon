from flask import Flask, jsonify, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from datetime import timedelta
import mysql.connector
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.urandom(24)  # Generate a strong random key

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)  # Initialize Flask-Session
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Session expires after 1 day
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Protect against CSRF

# Add CORS headers with credentials support
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp

app.after_request(add_cors_headers)

@app.route("/api/<path:path>", methods=["OPTIONS"])
def handle_options(path):
    response = jsonify({"message": "CORS preflight"})
    return add_cors_headers(response)

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="34.136.163.31",
        user="admin",
        password="Kv135791!",
        database="authen"
    )

# Register
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"message": "Account already exists."}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    cursor.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (username, hashed_pw))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Registered successfully!"}), 201

# Login
@app.route("/api/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return jsonify({"message": "Send POST with JSON {username, password}"})
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        session.clear()  # Clear any existing session
        session.permanent = True  # Make the session persistent
        session["logged_in"] = True
        session["username"] = username
        session["user_id"] = user["id"]  # Store user ID for security
        return jsonify({
            "message": "Log in successfully!",
            "username": username,
            "isLoggedIn": True
        })
    else:
        return jsonify({"message": "Wrong account or password!"}), 401

# Check login
@app.route("/api/check-session", methods=["GET"])
def check_login():
    is_logged_in = session.get("logged_in", False)
    username = session.get("username", None)
    
    return jsonify({
        "isLoggedIn": is_logged_in,
        "username": username,
        "message": f"Hello {username}, you are logged in!" if is_logged_in else "Not logged in"
    }), 200 if is_logged_in else 401

# Logout
@app.route("/api/logout", methods=["POST"])
def logout():
    if not session.get("logged_in"):
        return jsonify({"message": "Not logged in"}), 401
        
    session.clear()  # Clear entire session
    return jsonify({
        "message": "Logged out successfully",
        "isLoggedIn": False
    })

if __name__ == "__main__":
    app.run(debug=True, port=3000)
