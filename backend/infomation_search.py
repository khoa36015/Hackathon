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
        {"id": key, "ten": data["ten"], "mo_ta": data["mo_ta"]}
        for key, data in dulieu.items()
    ]
    return jsonify(result)

# ✅ Lấy chi tiết tỉnh theo id (ví dụ: /api/province/an_giang)
@app.route('/api/province/<province_id>', methods=['GET'])
def get_province_detail(province_id):
    province = dulieu.get(province_id.lower())
    if not province:
        abort(404, description="Không tìm thấy tỉnh này.")
    return jsonify(province)

# ✅ Tìm kiếm theo tên (ví dụ: /api/search?name=can tho)
@app.route('/api/search', methods=['GET'])
def search_province():
    name = request.args.get('name', '').lower()
    results = [
        {"id": key, "ten": info["ten"], "mo_ta": info["mo_ta"]}
        for key, info in dulieu.items()
        if name in info["ten"].lower()
    ]
    if not results:
        abort(404, description="Không tìm thấy tỉnh nào phù hợp.")
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=1311)
