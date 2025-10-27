from flask import Flask,jsonify,request

import mysql.connector

from datetime import datetime 

app = Flask(__name__)

def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp
#connect mysql
def get_db_connection():
        return mysql.connector.connect(
        host="34.136.163.31",
        user="admin",
        password="Kv135791!",
        database="Authen"
        )

    #gui API feedback
@app.route("/api/feedback",methods=['POST'])
def send_feedback():
     data=request.get_json()

     username=data.get('username')

     message=data.get('message')

     rating=data.get('rating')

     if not message: 
        return jsonify({'message':'lack of feedback content!'}), 400


     conn=get_db_connection()
     cursor=conn.cursor(dictionary=True)

     try:
         cursor.execute(
            "INSERT INTO feedbacks(username, message, rating, created_at) VALUES (%s, %s, %s, %s)",
            (username, message, rating, datetime.now())
         )
         conn.commit()
         return jsonify({"message":"Thanks for your feedback!"}), 201
     except Exception as e:
         return jsonify({"error": str(e)}), 500
     finally:
         cursor.close()
         conn.close()

@app.route("/api/feedbacks",methods=['GET'])
def get_feedbacks():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT username, message, rating, created_at FROM feedbacks ORDER BY created_at DESC"
            )
            results = cursor.fetchall()
            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

if __name__=='__main__':
  app.run(debug=True,port=36)