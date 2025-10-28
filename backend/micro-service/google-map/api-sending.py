from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# === DÁN DỮ LIỆU CỦA BẠN Ở ĐÂY =========================
# dulieu = { ... }  # <-- paste biến dulieu chuẩn hóa của bạn
# ========================================================

# Danh sách mã tỉnh thuộc miền Tây (trùng với key trong dulieu)
MEKONG_KEYS = [
    "an_giang", "kien_giang", "ben_tre", "can_tho", "ca_mau",
    "dong_thap", "soc_trang", "haugiang", "travinh", "baclieu",
    "vinhlong", "longan", "tiengiang"
]

def pick_fields(province_id: str, data: dict) -> dict:
    """Chuẩn hóa record trả về cho frontend."""
    return {
        "id": province_id,  # id = mã tỉnh (key)
        "ten": data.get("ten"),
        "mo_ta": data.get("mo_ta"),
        "anh_dai_dien": data.get("anh_dai_dien"),
        "so_dia_diem": len(data.get("dia_diem", {})),
        "so_mon_an": len(data.get("mon_an", {})),
        "van_hoa": data.get("van_hoa", [])
    }

@app.get("/api/ai/mekong")
def api_random_mekong():
    # Đọc tham số count, mặc định 6
    try:
        count = int(request.args.get("count", 6))
    except ValueError:
        count = 6

    # Lọc những key miền Tây có thật trong dulieu
    available = [k for k in MEKONG_KEYS if k in dulieu]
    if not available:
        return jsonify({"error": "dulieu rỗng hoặc thiếu các tỉnh miền Tây"}), 500

    # Ràng buộc count hợp lệ
    count = max(1, min(count, len(available)))

    # Lấy ngẫu nhiên
    chosen_ids = random.sample(available, count)

    # Biến đổi dữ liệu trả ra
    results = [pick_fields(pid, dulieu[pid]) for pid in chosen_ids]

    return jsonify({
        "count": count,
        "ket_qua": results
    })

if __name__ == "__main__":
    # Chạy local: http://127.0.0.1:8000/api/ai/mekong?count=6
    app.run(host="0.0.0.0", port=8000, debug=True)
