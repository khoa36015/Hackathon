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

# ✅ Tìm kiếm theo tên tỉnh
@app.route('/api/search', methods=['GET'])
def search_province():
    name = request.args.get('name', '').lower()
    if not name:
        abort(400, description="Thiếu tham số name.")
    results = [
        {"id": key, **info}
        for key, info in dulieu.items()
        if name in info["ten"].lower()
    ]
    if not results:
        abort(404, description="Không tìm thấy tỉnh nào phù hợp.")
    return jsonify(results)

# ✅ Tìm kiếm theo hashtag trong địa điểm / món ăn
@app.route('/api/search/hashtag', methods=['GET'])
def search_by_hashtag():
    tag = request.args.get('tag', '').strip()
    if not tag:
        abort(400, description="Thiếu tham số tag. Ví dụ: /api/search/hashtag?tag=#kham_pha")

    # chấp nhận cả "#kham_pha" và "kham_pha"
    tag_lower = tag.lower()
    if not tag_lower.startswith("#"):
        tag_lower = "#" + tag_lower

    results = []

    for province_id, province_data in dulieu.items():
        province_name = province_data.get("ten", province_id)
        matched_dia_diem = []
        matched_mon_an = []

        # 🔎 duyệt địa điểm
        dia_diem = province_data.get("dia_diem", {})
        for dd_name, dd_data in dia_diem.items():
            dd_tags = [t.lower() for t in dd_data.get("hashtags", [])]
            if tag_lower in dd_tags:
                matched_dia_diem.append({
                    "ten": dd_name,
                    "mo_ta": dd_data.get("mo_ta", ""),
                    "anh": dd_data.get("anh", {}),
                    "hashtags": dd_data.get("hashtags", [])
                })

        # 🔎 duyệt món ăn
        mon_an = province_data.get("mon_an", {})
        for mon_name, mon_data in mon_an.items():
            mon_tags = [t.lower() for t in mon_data.get("hashtags", [])]
            if tag_lower in mon_tags:
                matched_mon_an.append({
                    "ten": mon_name,
                    "mo_ta": mon_data.get("mo_ta", ""),
                    "anh": mon_data.get("anh", {}),
                    "hashtags": mon_data.get("hashtags", [])
                })

        # nếu tỉnh này có ít nhất 1 match thì đưa vào kết quả
        if matched_dia_diem or matched_mon_an:
            results.append({
                "province_id": province_id,
                "province_name": province_name,
                "dia_diem": matched_dia_diem,
                "mon_an": matched_mon_an
            })

    if not results:
        abort(404, description="Không tìm thấy địa điểm/món ăn nào theo hashtag này.")

    return jsonify({
        "hashtag": tag_lower,
        "count": len(results),
        "results": results
    })


if __name__ == "__main__":
    app.run(debug=True, port=1311)
