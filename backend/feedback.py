from flask import Flask, jsonify, request
import mysql.connector
from datetime import datetime 

app = Flask(__name__)

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

#connect mysql
def get_db_connection():
    return mysql.connector.connect(
        host="34.136.163.31",
        user="admin",
        password="Kv135791!",
        database="feedback" 
    )

#gui API feedback
@app.route("/api/feedback", methods=['POST'])
def send_feedback():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'Invalid JSON data'}), 400

        username = data.get('username')
        message = data.get('message')
        rating = data.get('rating')

        # kiem tra danh gia
        if rating is not None and not isinstance(rating, (int, float)):
            return jsonify({'message': 'Rating must be a number'}), 400

        if not message: 
            return jsonify({'message':'Feedback content is required!'}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                "INSERT INTO feedbacks(username, message, rating, created_at) VALUES (%s, %s, %s, %s)",
                (username, message, rating, datetime.now())
            )
            conn.commit()
            return jsonify({"message": "Thanks for your feedback!", "success": True}), 201
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e), "success": False}), 500
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        return jsonify({"error": "Invalid request", "message": str(e), "success": False}), 400

@app.route("/api/feedbacks", methods=['GET'])
def get_feedbacks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT username, message, rating, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') as created_at "
                "FROM feedbacks ORDER BY created_at DESC"
            )
            results = cursor.fetchall()
            
            # convert sang json
            formatted_results = [{
                'username': r['username'],
                'message': r['message'],
                'rating': float(r['rating']) if r['rating'] else None,
                'created_at': r['created_at']
            } for r in results]
            
            return jsonify({
                "success": True,
                "data": formatted_results
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": "Database error",
                "message": str(e)
            }), 500
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Server error",
            "message": str(e)
        }), 500

if __name__=='__main__':
  app.run(debug=True,port=3600)