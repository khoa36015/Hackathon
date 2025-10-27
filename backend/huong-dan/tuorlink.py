from flask import Flask,jsonyfy,request
import mysql.connector
app=Flask(__name__)

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

        
@app.route("/api/tour",methods=['GET'])
def get_tour():
    return jsonify(tours)


