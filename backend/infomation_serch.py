from flask import Flask, jsonify, request, abort
import mysql.connector
from data import provinces
from flask_cors import CORS

app = Flask(__name__)

# Bật CORS để frontend (React/Vue/HTML...) gọi được API
CORS(app)

#  Hàm thêm header CORS vào response (để chắc chắn không bị lỗi CORS)
@app.after_request
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp

def get_db_connection():
    return mysql.connector.connect(
        host="34.136.163.31",
        user="admin",
        password="Kv135791!",
        database="Authen"
    )

#api all tinh mien tay
@app.route('/api/provinces', methods=['GET'])
def get_provinces():
    result = [
        {"id": key, "ten": data["ten"], "mo_ta": data["mo_ta"]}
        for key, data in provinces.items()
    ]
    return jsonify(result)

#api chi tiet tinh theo id
@app.route('/api/province/<province_id>', methods=['GET'])
def get_province_detail(province_id):
    province = provinces.get(province_id.lower())
    if not province:
        abort(404, description="Không tìm thấy tỉnh này.")
    return jsonify(province)

# api tìm kiếm tỉnh theo tên
@app.route('/api/search', methods=['GET'])
def search_province():
    name = request.args.get('name', '').lower()
    for key, info in provinces.items():
        if name in info["ten"].lower():
            return jsonify(info)
    abort(404, description="Không tìm thấy tỉnh nào phù hợp.")

if __name__ == "__main__":
    app.run(debug=True, port=1311)
