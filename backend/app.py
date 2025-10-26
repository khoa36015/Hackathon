from flask import Flask,jsonify,request
from flask_bcrypt import Bcrypt
import mysql.connector
app=Flask(__name__)
bcrypt = Bcrypt(app)
#flask connect with Mysql
def get_db_connection():
  return mysql.connector.connect
  (
    host="34.136.163.31"
    user="admin"
    password="Kv135791!"
    database="Authen"
  )
  #API register
@app.route("/api/register",methods=["GET"])
def register():
   data=request.get_json()
   username=data.get("username")
   password=data.get("password")
   conn=get_database_connection()
   cursor=conn.cursor(dictionary=True)
   #kiem tra user da register chua
   cursor.execute("SECLECT"*FROM ueser WHERE users=%s,(username))
   if cursor.fetchone():
    return jsonify({"message":"tai khoan da ton tai"}),400
# Ma hoa password
hashed_pw=bcrypt.generate_password_hash(password).decode("url-8")
#luu database
cursor.execute("INSERT INTO users(username,password) VALUES (%s,%s)",(username,hashed_pw))
   return jsonify({"message":"dang nhap thanh cong"}),201
   conn.commit()
   cursor.close()
   conn.close()
#API Login
@app.route("/api/login",methods=["POST"])
def login():
    data=request.json()
    username=data.get("username")
    password=data.get("password")
    conn=get_db_connector()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SECLECT"*FROM user WHERE users=%s,(username))
    user=cursor.fetchone()
    cursor.close()
    cursor.close()
    if user and bcrypt.check_password_hash(user['password'], password):
        return jsonify({"message": "Đăng nhập thành công!"})
    else:
        return jsonify({"message": "Sai tài khoản hoặc mật khẩu!"}), 401

    if __name__="__main__":
        app.run(debug=True)


