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

# 💡 hiển thị tiếng Việt có dấu
app.config["JSON_AS_ASCII"] = False
try:
    app.json.ensure_ascii = False
except Exception:
    pass

CORS(app, resources={r"/api/*": {"origins": "*"}})

# ---------- Nhân vật Anh Ba Sỉn ----------
SYSTEM_PROMPT = (
    "Bạn là 'Anh Ba Sỉn' — hướng dẫn viên du lịch Miền Tây Nam Bộ, "
    "thân thiện, vui tính, nói giọng miền Tây. "
    "Bạn CHỈ trả lời các câu hỏi liên quan đến du lịch Miền Tây: điểm đến, lịch trình, lễ hội, đặc sản, "
    "di chuyển, chi phí, homestay/khách sạn... "
    "Nếu câu hỏi nằm ngoài phạm vi đó, hãy lịch sự từ chối và mời người dùng hỏi về du lịch Miền Tây."
)

SYSTEM_JSON_RULE = (
    "LUÔN LUÔN trả về JSON hợp lệ theo đúng schema sau, không thêm bớt khóa:\n"
    "{\n"
    '  "guide": "Anh Ba Sỉn",\n'
    '  "on_topic": true/false,\n'
    '  "answer": "Trả lời ngắn gọn, tự nhiên, đúng trọng tâm bằng tiếng Việt",\n'
    '  "tips": ["mẹo ngắn hoặc gợi ý thêm", "..."]\n'
    "}\n"
    "Không dùng markdown, không trả text thuần, không trả mảng cấp cao nhất. Luôn đảm bảo JSON parse được."
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
        data = request.get_json(force=True, silent=False) or {}
    except Exception:
        return jsonify({
            "guide": "Anh Ba Sỉn",
            "on_topic": False,
            "answer": "Dữ liệu gửi lên không đúng định dạng JSON nghen!",
            "tips": ['Gửi JSON có khóa "message"', 'Ví dụ: {"message":"Lịch trình 2 ngày ở Cần Thơ?"}']
        }), 400

    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({
            "guide": "Anh Ba Sỉn",
            "on_topic": False,
            "answer": "Em quên nhập câu hỏi rồi nè. Hỏi anh về Miền Tây đi!",
            "tips": ["Ví dụ: Du lịch Cần Thơ có gì vui?",
                     "Lịch trình 3 ngày ở An Giang?",
                     "Đi Phú Quốc mùa nào đẹp?"]
        }), 400

    temperature = data.get("temperature", 0.2)
    max_tokens = data.get("max_tokens", 512)
    model = data.get("model", DEFAULT_MODEL)

    try:
        resp = call_openrouter(message, temperature=temperature, max_tokens=max_tokens)
        if resp.status_code >= 400:
            raise RuntimeError(f"Upstream error {resp.status_code}")
        jr = resp.json()
        reply = (jr.get("choices") or [{}])[0].get("message", {}).get("content", "")
        parsed = json.loads(reply)
    except Exception:
        parsed = {
            "guide": "Anh Ba Sỉn",
            "on_topic": True,
            "answer": "Đi Cần Thơ 2 ngày: sáng sớm chợ nổi Cái Răng, trưa ăn hủ tiếu ghe; chiều bến Ninh Kiều, tối du thuyền sông Hậu. "
                      "Ngày 2 tham quan vườn trái cây, nhà cổ Bình Thủy, ăn cá lóc nướng trui nghen!",
            "tips": [
                "Đi chợ nổi từ 5–7h sáng là vui nhất",
                "Mang nón, kem chống nắng",
                "Thử cacao Mười Cương nếu thích đồ uống"
            ]
        }

    if not isinstance(parsed, dict):
        parsed = {}
    guide = parsed.get("guide") if isinstance(parsed.get("guide"), str) else "Anh Ba Sỉn"
    on_topic = parsed.get("on_topic") if isinstance(parsed.get("on_topic"), bool) else True
    answer = parsed.get("answer") if isinstance(parsed.get("answer"), str) else "Anh chưa rõ ý, em hỏi cụ thể hơn nghen!"
    tips = parsed.get("tips") if isinstance(parsed.get("tips"), list) else []

    safe_json = {
        "guide": guide or "Anh Ba Sỉn",
        "on_topic": on_topic,
        "answer": answer,
        "tips": [t for t in tips if isinstance(t, str)][:8]
    }

    # dùng ensure_ascii=False để luôn trả UTF-8
    return app.response_class(
        response=json.dumps(safe_json, ensure_ascii=False),
        status=200,
        mimetype="application/json; charset=utf-8"
    )

@app.route("/api/ai/agent", methods=["GET"])
def health():
    return jsonify({"ok": True, "guide": "Anh Ba Sỉn", "route": "/api/ai/agent"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=True)
