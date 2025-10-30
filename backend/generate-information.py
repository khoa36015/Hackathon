from flask import Flask, jsonify
from data1 import dulieu
import random

app = Flask(__name__)

@app.route("/api/random-provinces", methods=["GET"])
def random_provinces():
    province_keys = list(dulieu.keys())

    # Random 6 tỉnh khác nhau
    selected = random.sample(province_keys, 6)

    # Gán ID từ 1 đến 6 và định dạng JSON theo yêu cầu
    provinces = {}
    for i, key in enumerate(selected, start=1):
        provinces[str(i)] = {
            "tinh": key,
            "data": dulieu[key]
        }

    return jsonify({
        "total": 6,
        "provinces": provinces
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
# ... giữ nguyên phần import, app, CORS, /api/ai/agent ở trên

# ---- dữ liệu mẫu cho miền Tây ----
BASE_PLACES = {
    "cantho": [
        {"id": "cho-noi-cai-rang", "name": "Chợ nổi Cái Răng", "cost": "low", "duration_h": 2, "best_time": "morning"},
        {"id": "ben-ninh-kieu", "name": "Bến Ninh Kiều", "cost": "low", "duration_h": 1, "best_time": "afternoon"},
        {"id": "nha-co-binh-thuy", "name": "Nhà cổ Bình Thủy", "cost": "medium", "duration_h": 1, "best_time": "morning"},
        {"id": "vuon-trai-cay", "name": "Vườn trái cây", "cost": "medium", "duration_h": 2, "best_time": "afternoon"},
        {"id": "du-thuyen-song-hau", "name": "Du thuyền sông Hậu", "cost": "high", "duration_h": 2, "best_time": "evening"},
    ],
    "angiang": [
        {"id": "nui-sam", "name": "Núi Sam - Châu Đốc", "cost": "low", "duration_h": 2, "best_time": "morning"},
        {"id": "mienh-ba-chua-xu", "name": "Miếu Bà Chúa Xứ", "cost": "low", "duration_h": 1, "best_time": "morning"},
        {"id": "tra-su", "name": "Rừng tràm Trà Sư", "cost": "medium", "duration_h": 3, "best_time": "afternoon"},
        {"id": "lang-cham", "name": "Làng Chăm Châu Phong", "cost": "low", "duration_h": 1, "best_time": "afternoon"},
    ]
}

def pick_places(province: str, budget: str, days: int):
    """Chọn điểm phù hợp với tỉnh, ngân sách và số ngày (rule đơn giản)."""
    province = province.lower()
    places = BASE_PLACES.get(province, [])
    if not places:
        return []

    # lọc theo budget
    if budget == "low":
        cand = [p for p in places if p["cost"] in ("low",)]
    elif budget == "medium":
        cand = [p for p in places if p["cost"] in ("low", "medium")]
    else:  # high
        cand = places[:]  # lấy hết

    # đơn giản: mỗi ngày tối đa 3 điểm
    max_points = days * 3
    return cand[:max_points]


@app.route("/api/itinerary/generate", methods=["POST"])
def generate_itinerary():
    """
    Body mẫu:
    {
      "province": "cantho",
      "budget": "low",   # low | medium | high
      "days": 2,
      "nights": 1
    }
    """
    data = request.get_json(force=True, silent=True) or {}
    province = (data.get("province") or "cantho").lower()
    budget = (data.get("budget") or "medium").lower()
    days = int(data.get("days") or 1)
    nights = int(data.get("nights") or (days - 1 if days > 1 else 0))

    picked = pick_places(province, budget, days)

    # build lịch trình theo ngày
    itinerary = []
    idx = 0
    for d in range(1, days + 1):
        day_plan = {
            "day": d,
            "title": f"Ngày {d} tại {province.title()}",
            "items": []
        }
        # mỗi ngày tối đa 3 điểm
        for _ in range(3):
            if idx >= len(picked):
                break
            place = picked[idx]
            day_plan["items"].append({
                "time": guess_time(place.get("best_time")),
                "place_id": place["id"],
                "place_name": place["name"],
                "cost_level": place["cost"],
                "note": f"Điểm gợi ý phù hợp chi phí {budget}"
            })
            idx += 1
        itinerary.append(day_plan)

    return jsonify({
        "province": province,
        "budget": budget,
        "days": days,
        "nights": nights,
        "itinerary": itinerary
    }), 200


def guess_time(best_time: str):
    """Đổi best_time sang giờ cố định để front-end vẽ timeline."""
    if best_time == "morning":
        return "08:00"
    if best_time == "afternoon":
        return "14:00"
    if best_time == "evening":
        return "19:00"
    return "09:00"
