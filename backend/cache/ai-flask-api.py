import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openai/gpt-4o-mini").strip()

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is missing in .env")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ---------- Nhân vật Anh Ba Sỉn ----------
SYSTEM_PROMPT = (
    "Bạn là 'Anh Ba Sỉn' — hướng dẫn viên du lịch Miền Tây Nam Bộ, "
    "thân thiện, vui tính, nói giọng miền Tây. "
    "Bạn chỉ trả lời các câu hỏi về du lịch Miền Tây: địa điểm, món ăn, lễ hội, đặc sản, "
    "chi phí, di chuyển, gợi ý lịch trình... "
    "Nếu người dùng hỏi ngoài chủ đề này, hãy lịch sự nói rằng bạn chỉ biết về du lịch Miền Tây."
)

SYSTEM_JSON_RULE = (
    "LUÔN LUÔN trả về JSON hợp lệ với cấu trúc:\n"
    "{\n"
    '  "guide": "Anh Ba Sỉn",\n'
    '  "on_topic": true/false,\n'
    '  "answer": "Trả lời ngắn gọn, tự nhiên, đúng trọng tâm bằng tiếng Việt",\n'
    '  "tips": ["mẹo ngắn hoặc gợi ý thêm", "..."]\n'
    "}\n"
    "Không markdown, không text thuần, luôn là JSON parse được."
)

def call_openrouter(message: str, temperature: float = 0.2, max_tokens: int = 512):
    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": SYSTEM_JSON_RULE},
            {"role": "user", "content": message}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"}
    }

    return requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "Anh-Ba-Sin-Agent"
        },
        json=payload,
        timeout=60
    )

@app.route("/api/ai/agent", methods=["POST"])
def ai_agent():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({
            "guide": "Anh Ba Sỉn",
            "on_topic": False,
            "answer": "Dữ liệu gửi lên không đúng định dạng JSON nghen!",
            "tips": ["Gửi JSON có khóa 'message'", "Ví dụ: {'message':'Du lịch Cần Thơ có gì vui?'}"]
        }), 400

    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({
            "guide": "Anh Ba Sỉn",
            "on_topic": False,
            "answer": "Em quên chưa nói muốn hỏi gì nè!",
            "tips": ["Ví dụ: 'Ăn gì ở Cần Thơ'", "Hoặc: 'Lịch trình 2 ngày ở Bến Tre'"]
        }), 400

    try:
        resp = call_openrouter(message)
        jr = resp.json()
        reply = (jr.get("choices") or [{}])[0].get("message", {}).get("content", "")
        parsed = json.loads(reply)
    except Exception:
        parsed = {
            "guide": "Anh Ba Sỉn",
            "on_topic": True,
            "answer": "Đi Cần Thơ 2 ngày: Sáng đi chợ nổi Cái Răng, chiều bến Ninh Kiều, tối du thuyền sông Hậu; ngày 2 tham quan vườn trái cây, nhà cổ Bình Thủy, ăn cá lóc nướng trui nghen!",
            "tips": [
                "Đi chợ nổi 5–7h sáng là vui nhất",
                "Mang nón, kem chống nắng",
                "Thử cacao Mười Cương nếu thích đồ uống"
            ]
        }

    # đảm bảo đúng định dạng
    if not isinstance(parsed, dict):
        parsed = {}
    safe_json = {
        "guide": parsed.get("guide", "Anh Ba Sỉn"),
        "on_topic": parsed.get("on_topic", True),
        "answer": parsed.get("answer", "Anh chưa rõ ý, nói lại nghen!"),
        "tips": parsed.get("tips", [])
    }

    return jsonify(safe_json), 200

@app.route("/api/ai/agent", methods=["GET"])
def health():
    return jsonify({"ok": True, "guide": "Anh Ba Sỉn", "route": "/api/ai/agent"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=True)
