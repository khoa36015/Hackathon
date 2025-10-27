from flask import Flask, jsonify, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "dev-secret-key"  # keep secret in production

# Add CORS headers
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
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
        session["logged_in"] = True
        session["username"] = username
        return jsonify({"message": "Log in successfully!"})
    else:
        return jsonify({"message": "Wrong account or password!"}), 401

# Check login
@app.route("/", methods=["GET"])
def check_login():
    if not session.get("logged_in"):
        return jsonify({"message": "Please login first!"}), 401
    return jsonify({"message": f"Hello {session.get('username')}, you are logged in!"})

# Logout
@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    return jsonify({"message": "Logged out"})

if __name__ == "__main__":
    app.run(debug=True, port=30)
