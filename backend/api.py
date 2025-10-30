from flask import Flask, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from datetime import datetime, timedelta
import mysql.connector, os

app = Flask(__name__)
bcrypt = Bcrypt(app)

# ✅ key cố định để restart không mất session
app.secret_key = "super-secret-dev-key"

# ✅ cấu hình session cho DEV (http, khác port)
app.config.update(
    SESSION_TYPE='filesystem',
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',   # Lax an toàn và vẫn gửi trong hầu hết trường hợp
    SESSION_COOKIE_SECURE=False      # dev http => False
)
Session(app)

# ---------- CORS ----------
@app.after_request
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "http://127.0.0.1:5500")
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp

@app.route("/api/<path:path>", methods=["OPTIONS"])
def handle_options(path):
    return add_cors_headers(jsonify({"message": "ok"}))

# ---------- DB ----------
def db_conn(db_name):
    return mysql.connector.connect(
        host="34.136.163.31",
        user="admin",
        password="Kv135791!",
        database=db_name
    )

# ---------- AUTH ----------
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    u, p = data.get("username"), data.get("password")
    if not u or not p:
        return jsonify({"message": "Missing username or password"}), 400
    conn = db_conn("authen"); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE username=%s", (u,))
    if cur.fetchone():
        return jsonify({"message": "Account exists"}), 400
    hashed = bcrypt.generate_password_hash(p).decode()
    cur.execute("INSERT INTO users(username,password) VALUES(%s,%s)", (u, hashed))
    conn.commit(); cur.close(); conn.close()
    return jsonify({"message": "Registered!"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    u, p = data.get("username"), data.get("password")
    if not u or not p:
        return jsonify({"message": "Missing username or password"}), 400
    conn = db_conn("authen"); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE username=%s", (u,))
    user = cur.fetchone()
    cur.close(); conn.close()
    if user and bcrypt.check_password_hash(user["password"], p):
        session.clear()
        session.permanent = True
        session.update({"logged_in": True, "username": u, "user_id": user["id"]})
        return jsonify({"message": "Logged in", "isLoggedIn": True, "username": u})
    return jsonify({"message": "Wrong credentials"}), 401

@app.route("/api/check-session")
def check_session():
    if session.get("logged_in"):
        return jsonify({"isLoggedIn": True, "username": session["username"]})
    return jsonify({"isLoggedIn": False}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    if not session.get("logged_in"):
        return jsonify({"message": "Not logged in"}), 401
    session.clear()
    return jsonify({"message": "Logged out", "isLoggedIn": False})

# ---------- FEEDBACK ----------
@app.route("/api/feedback", methods=["POST"])
def feedback():
    d = request.get_json() or {}
    if not d.get("message"):
        return jsonify({"message": "Message required"}), 400
    rating = d.get("rating")
    if rating is not None and not isinstance(rating, (int, float)):
        return jsonify({"message": "Rating must be number"}), 400

    # changed: use dictionary cursor to inspect created_at and avoid duplicate inserts
    conn = db_conn("feedback"); cur = conn.cursor(dictionary=True)

    # check recent duplicate: same username+message inserted very recently (e.g. within 5 seconds)
    try:
        cur.execute(
            "SELECT id, created_at FROM feedbacks WHERE username=%s AND message=%s ORDER BY created_at DESC LIMIT 1",
            (d.get("username"), d["message"])
        )
        prev = cur.fetchone()
        if prev and isinstance(prev.get("created_at"), datetime):
            if datetime.now() - prev["created_at"] < timedelta(seconds=5):
                cur.close(); conn.close()
                # benign response: treat as already-received to prevent duplicate on refresh
                return jsonify({"message": "Duplicate ignored"}), 200

        # proceed with insert if not a recent duplicate
        cur.execute(
            "INSERT INTO feedbacks(username,message,rating,created_at) VALUES (%s,%s,%s,%s)",
            (d.get("username"), d["message"], rating, datetime.now())
        )
        conn.commit()
    finally:
        cur.close(); conn.close()

    return jsonify({"message": "Feedback saved"}), 201

@app.route("/api/feedbacks")
def feedbacks():
    conn = db_conn("feedback"); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT username,message,rating,DATE_FORMAT(created_at,'%Y-%m-%d %H:%i:%s') AS created_at FROM feedbacks ORDER BY created_at DESC")
    data = cur.fetchall()
    cur.close(); conn.close()
    return jsonify({"success": True, "data": data})

if __name__ == "__main__":
    # ❗ quan trọng: tắt reloader để không chạy 2 process
    app.run(debug=True, port=3000, use_reloader=False)