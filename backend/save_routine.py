from flask import Flask, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)

# Đường dẫn file JSON tạm (dùng như DB nhỏ)
ITINERARY_FILE = "itineraries.json"

# Hàm đọc file JSON
def read_data():
    if not os.path.exists(ITINERARY_FILE):
        return []
    with open(ITINERARY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Hàm ghi file JSON
def write_data(data):
    with open(ITINERARY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ✅ API 1: Lưu lịch trình đã chỉnh sửa
@app.route("/api/itinerary/save", methods=["POST"])
def save_itinerary():
    data = read_data()
    new_itinerary = request.get_json()

    # Kiểm tra dữ liệu gửi lên
    if not new_itinerary or "user_id" not in new_itinerary or "title" not in new_itinerary:
        return jsonify({"error": "Missing user_id or title"}), 400

    # Nếu có id thì update, không thì tạo mới
    itinerary_id = new_itinerary.get("id")
    if itinerary_id:
        for item in data:
            if item["id"] == itinerary_id:
                item.update(new_itinerary)
                item["updated_at"] = datetime.now().isoformat()
                write_data(data)
                return jsonify({"message": "Itinerary updated successfully"}), 200
    else:
        new_itinerary["id"] = str(len(data) + 1)
        new_itinerary["created_at"] = datetime.now().isoformat()
        new_itinerary["updated_at"] = datetime.now().isoformat()
        data.append(new_itinerary)
        write_data(data)
        return jsonify({"message": "Itinerary saved successfully", "id": new_itinerary["id"]}), 201

# ✅ API 2: Lấy danh sách lịch trình của user (đã login)
@app.route("/api/itinerary/mine", methods=["GET"])
def get_my_itineraries():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    data = read_data()
    user_itineraries = [i for i in data if i["user_id"] == user_id]
    return jsonify(user_itineraries), 200

# ✅ API 3: Lấy chi tiết 1 lịch trình
@app.route("/api/itinerary/<id>", methods=["GET"])
def get_itinerary_detail(id):
    data = read_data()
    for i in data:
        if i["id"] == id:
            return jsonify(i), 200
    return jsonify({"error": "Itinerary not found"}), 404

# ✅ CORS (cho frontend kết nối)
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

if __name__ == "__main__":
    app.run(debug=True)
