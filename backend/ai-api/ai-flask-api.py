import os
import json
import re
import unicodedata
import random
from typing import Any, Dict, List, Optional

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openai/gpt-4o-mini").strip()
DEFAULT_SYSTEM = os.getenv(
    "DEFAULT_SYSTEM",
    "You only output compact, valid JSON. No explanations, no markdown, no extra keys. If unsure, return {}."
).strip()

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is missing in .env")

MEKONG_PROVINCES = [
    "an giang", "bac lieu", "ben tre", "ca mau", "can tho", "dong thap",
    "hau giang", "kien giang", "long an", "soc trang", "tien giang", "tra vinh",
    "vinh long"
]

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


def vn_to_ascii_lower(text: str) -> str:
    if not isinstance(text, str):
        return text
    nfkd = unicodedata.normalize("NFKD", text)
    no_acc = "".join(ch for ch in nfkd if not unicodedata.combining(ch))
    low = no_acc.lower()
    low = re.sub(r"[^a-z ]+", "", low).strip()
    low = re.sub(r"\s+", " ", low)
    return low


def openrouter_chat(payload: Dict[str, Any]) -> requests.Response:
    return requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "AI-Agent-JSON-Only"
        },
        json=payload,
        timeout=60
    )


def offline_mekong_six():
    return {"tinh": random.sample(MEKONG_PROVINCES, 6)}


def enforce_mekong6(obj):
    if not isinstance(obj, dict):
        return {"tinh": random.sample(MEKONG_PROVINCES, 6)}
    reply = obj.get("reply") or obj
    tinh = reply.get("tinh") if isinstance(reply, dict) else None
    if not isinstance(tinh, list):
        tinh = []
    cleaned = []
    seen = set()
    for t in tinh:
        if isinstance(t, str):
            tt = vn_to_ascii_lower(t)
            if tt in MEKONG_PROVINCES and tt not in seen:
                seen.add(tt)
                cleaned.append(tt)
    remaining = [p for p in MEKONG_PROVINCES if p not in seen]
    random.shuffle(remaining)
    while len(cleaned) < 6 and remaining:
        cleaned.append(remaining.pop())
    return {"tinh": cleaned}


@app.route("/api/ai/agent", methods=["POST"])
def ai_agent():
    try:
        data = request.get_json(force=True, silent=False) or {}
    except Exception:
        return jsonify({"error": "Invalid JSON body"}), 400

    message: str = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Missing 'message'"}), 400

    payload = {
        "model": data.get("model", DEFAULT_MODEL),
        "messages": [
            {"role": "system", "content": DEFAULT_SYSTEM},
            {"role": "user", "content": message}
        ],
        "temperature": data.get("temperature", 0),
        "max_tokens": data.get("max_tokens", 512),
        "response_format": {"type": "json_object"}
    }

    try:
        resp = openrouter_chat(payload)
    except requests.Timeout:
        return jsonify(offline_mekong_six()), 504
    except Exception:
        return jsonify(offline_mekong_six()), 502

    if resp.status_code >= 400:
        return jsonify(offline_mekong_six()), 502

    try:
        jr = resp.json()
        reply = (jr.get("choices") or [{}])[0].get("message", {}).get("content", "")
        parsed = json.loads(reply)
    except Exception:
        parsed = offline_mekong_six()

    parsed = enforce_mekong6(parsed)
    return jsonify(parsed), 200


@app.route("/api/ai/agent", methods=["GET"])
def health():
    return jsonify({"ok": True, "route": "/api/ai/agent"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=True)
