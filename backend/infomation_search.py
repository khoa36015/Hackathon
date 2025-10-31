from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from data1 import dulieu  # ✅ import đúng dữ liệu từ file data1.py

app = Flask(__name__)
CORS(app)

@app.after_request
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp

# ✅ Lấy tất cả tỉnh
@app.route('/api/provinces', methods=['GET'])
def get_provinces():
    result = [
        {"id": key, **data}  # Return all fields from data
        for key, data in dulieu.items()
    ]
    return jsonify(result)

# ✅ Lấy chi tiết tỉnh theo id
@app.route('/api/province/<province_id>', methods=['GET'])
def get_province_detail(province_id):
    province = dulieu.get(province_id.lower())
    if not province:
        abort(404, description="Không tìm thấy tỉnh này.")
    return jsonify({"id": province_id.lower(), **province})

# ✅ Tìm kiếm theo tên
@app.route('/api/search', methods=['GET'])
def search_province():
    name = request.args.get('name', '').lower()
    results = [
        {"id": key, **info}  # Return all fields from info
        for key, info in dulieu.items()
        if name in info["ten"].lower()
    ]
    if not results:
        abort(404, description="Không tìm thấy tỉnh nào phù hợp.")
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=1311)
