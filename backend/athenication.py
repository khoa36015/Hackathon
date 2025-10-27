from flask import Flask, jsonify, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)
bcrypt = Bcrypt(app)
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp
# flask connect with Mysql
def get_db_connection():
    return mysql.connector.connect(
        host="34.136.163.31",
        user="admin",
        password="Kv135791!",
        database="Authen"
    )

# API register
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # kiem tra user da register chua
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"message": "tai khoan da ton tai"}), 400
    
    # Ma hoa password
    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    
    # luu database
    cursor.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (username, hashed_pw))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "dang ky thanh cong"}), 201

# API Login
@app.route("/api/login", methods=["POST","GET"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user and bcrypt.check_password_hash(user['password'], password):
        session["username"] = request.form.get("username")
        return jsonify({"message": "Đăng nhập thành công!"})
    else:
        return jsonify({"message": "Sai tài khoản hoặc mật khẩu!"}), 401


#kiem tra nguoi dung da login vao hay chua
@app.route("/", methods=["GET"])
def check_login():
    if not session.get("logged_in"):
        return redirect('localhost://api/login')
    else:
        return jsonify({"message": "login successfully!"})
@app.route("/api/logout", methods=["POST"])
def logout():
    session[username] = None
    return redirect('localhost:80/login')
    

if __name__ == "__main__":
    app.run(debug=True,port=30)