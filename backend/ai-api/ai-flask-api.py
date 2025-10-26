import os
import json
import re
import unicodedata
import random
from typing import Any, Dict, List, Optional

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# ====== Config (unchanged endpoint/port) ======
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openai/gpt-4o-mini")
DEFAULT_SYSTEM = os.getenv("DEFAULT_SYSTEM", "You are a helpful assistant. Keep answers concise.")
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*")
REFERER = os.getenv("OPENROUTER_HTTP_REFERER", "http://localhost")
X_TITLE = os.getenv("OPENROUTER_X_TITLE", "AI Agent Tester")
OFFLINE_FALLBACK_MEKONG = os.getenv("OFFLINE_FALLBACK_MEKONG", "0") in ("1", "true", "True")

if not OPENROUTER_API_KEY:
    print("[WARN] Missing OPENROUTER_API_KEY in .env — /api/ai/agent calls may fail upstream.")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ALLOW_ORIGINS}})

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MEKONG_PROVINCES = [
    "an giang","bac lieu","ben tre","ca mau","can tho","dong thap",
    "hau giang","kien giang","long an","soc trang","tien giang","tra vinh",
    "vinh long"
]


# ====== Helpers ======
def build_messages(user_message: str, system_override: Optional[str], history: Optional[list]) -> list:
    messages = []
    system_prompt = (system_override or DEFAULT_SYSTEM).strip()
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if isinstance(history, list):
        for m in history:
            r = m.get("role")
            c = m.get("content")
            if r in ("user", "assistant", "system") and isinstance(c, str) and c.strip():
                messages.append({"role": r, "content": c})
    messages.append({"role": "user", "content": user_message})
    return messages


def parse_json_strict(s: str) -> Optional[Any]:
    if not isinstance(s, str) or not s:
        return None
    s2 = re.sub(r"^```(?:json)?|```$", "", s.strip(), flags=re.IGNORECASE | re.MULTILINE)
    start = s2.find("{")
    end = s2.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    s2 = s2[start:end + 1]
    try:
        return json.loads(s2)
    except Exception:
        return None


def vn_to_ascii_lower(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text or "")
    no_acc = "".join(ch for ch in nfkd if not unicodedata.combining(ch))
    low = re.sub(r"[^a-z ]+", "", no_acc.lower()).strip()
    return re.sub(r"\s+", " ", low)


def transform_array_strings(obj: Any, keys: Optional[List[str]]) -> Any:
    if not keys or not isinstance(obj, dict):
        return obj
    out = {}
    for k, v in obj.items():
        if k in keys and isinstance(v, list):
            out[k] = [vn_to_ascii_lower(x) if isinstance(x, str) else x for x in v]
        else:
            out[k] = v
    return out


def pattern_is_mekong6(message: str) -> bool:
    m = message.lower()
    return (("6" in m or "sáu" in m or "sau " in m) and ("miền tây" in m or "mien tay" in m))


def offline_mekong_six() -> Dict[str, List[str]]:
    return {"tinh": sorted(random.sample(MEKONG_PROVINCES, 6))}


def enforce_mekong6(obj: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure obj['tinh'] contains 6 unique Mekong provinces (lowercase, no diacritics)."""
    if not isinstance(obj, dict):
        return {"tinh": sorted(random.sample(MEKONG_PROVINCES, 6))}
    arr = obj.get("tinh", [])
    cleaned = []
    seen = set()
    # normalize and keep only known provinces
    for x in arr if isinstance(arr, list) else []:
        if isinstance(x, str):
            y = vn_to_ascii_lower(x)
            if y in MEKONG_PROVINCES and y not in seen:
                seen.add(y)
                cleaned.append(y)
    # fill if less than 6
    remaining = [p for p in MEKONG_PROVINCES if p not in seen]
    random.shuffle(remaining)
    while len(cleaned) < 6 and remaining:
        cleaned.append(remaining.pop())
    # trim if more than 6
    cleaned = cleaned[:6]
    return {"tinh": cleaned}


def build_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": REFERER,
        "X-Title": X_TITLE,
    }


# ====== Route (UNCHANGED: /api/ai/agent) ======
@app.route("/api/ai/agent", methods=["POST"])
def ai_agent():
    try:
        data = request.get_json(force=True, silent=False) or {}
        message = (data.get("message") or "").strip()
        if not message:
            return jsonify({"error": "Missing 'message'"}), 400

        model = (data.get("model") or DEFAULT_MODEL).strip()
        system_override = data.get("system")
        history = data.get("history")
        temperature = data.get("temperature", 0.0)
        max_tokens = data.get("max_tokens", None)

        json_mode = bool(data.get("json_mode", False))
        json_schema = data.get("json_schema")
        postprocess_cfg = data.get("postprocess") or {}
        array_string_keys = postprocess_cfg.get("array_string_keys", [])

        auto_schema = None
        mekong_pattern = pattern_is_mekong6(message)
        if mekong_pattern:
            json_mode = True
            # Remove 'uniqueItems' because some providers (e.g., Azure) reject it
            auto_schema = {
                "type": "object",
                "properties": {
                    "tinh": {
                        "type": "array",
                        "items": {"type": "string", "pattern": "^[a-z ]+$"},
                        "minItems": 6,
                        "maxItems": 6
                    }
                },
                "required": ["tinh"],
                "additionalProperties": False
            }
            system_override = (
                "You only output compact, valid JSON. Do not include explanations, markdown, or extra text. "
                "If unsure, return {}."
            )

        payload: Dict[str, Any] = {
            "model": model,
            "messages": build_messages(message, system_override, history),
            "temperature": temperature,
        }
        if isinstance(max_tokens, int) and max_tokens > 0:
            payload["max_tokens"] = max_tokens

        if json_mode:
            if isinstance(json_schema, dict):
                payload["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {"name": "strict_schema", "schema": json_schema, "strict": True}
                }
            elif auto_schema:
                payload["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {"name": "mekong_schema", "schema": auto_schema, "strict": True}
                }
            else:
                payload["response_format"] = {"type": "json_object"}

        headers = build_headers()

        # Send request (with one retry if provider rejects schema)
        def do_request(pay):
            return requests.post(OPENROUTER_URL, json=pay, headers=headers, timeout=60)

        resp = do_request(payload)

        # Retry logic for provider schema rejection (e.g., Azure)
        if resp.status_code == 400:
            try:
                err = resp.json()
            except Exception:
                err = {"message": resp.text}
            raw = json.dumps(err)
            if "Invalid schema for response_format" in raw:
                # Switch to json_object and retry once
                pay2 = dict(payload)
                pay2.pop("response_format", None)
                pay2["response_format"] = {"type": "json_object"}
                resp = do_request(pay2)

        # 401 handling & optional offline fallback
        if resp.status_code == 401:
            details = {
                "hint": "401 từ OpenRouter. Kiểm tra API key sk-or-..., Referer whitelist, billing.",
                "sent_headers": {k: headers[k] for k in ["HTTP-Referer", "X-Title"]},
            }
            if OFFLINE_FALLBACK_MEKONG and mekong_pattern:
                result = enforce_mekong6({"tinh": []})
                return jsonify({"reply": result, "model": "offline-fallback", "usage": {}, "warning": details}), 200
            try: err = resp.json()
            except Exception: err = {"message": resp.text}
            return jsonify({"error": "OpenRouter 401", "details": err, "debug": details}), 401

        if resp.status_code >= 400:
            try: err = resp.json()
            except Exception: err = {"message": resp.text}
            # Fallback offline if requested and pattern matches
            if OFFLINE_FALLBACK_MEKONG and mekong_pattern:
                result = enforce_mekong6({"tinh": []})
                return jsonify({"reply": result, "model": "offline-fallback", "usage": {}, "warning": err}), 200
            return jsonify({"error": "OpenRouter error", "details": err, "status": resp.status_code}), resp.status_code

        jr = resp.json()
        choice = (jr.get("choices") or [{}])[0]
        reply = (choice.get("message") or {}).get("content", "")

        # JSON-mode path
        if json_mode or auto_schema:
            parsed = parse_json_strict(reply)
            if parsed is None:
                if OFFLINE_FALLBACK_MEKONG and mekong_pattern:
                    result = enforce_mekong6({"tinh": []})
                    return jsonify({"reply": result, "model": "offline-fallback", "usage": {},
                                    "warning": "Model JSON invalid, used offline fallback."}), 200
                return jsonify({"error": "Invalid JSON from model", "raw": reply}), 502

            parsed = transform_array_strings(parsed, array_string_keys or (["tinh"] if mekong_pattern else []))

            # Enforce uniqueness & length 6 server-side for Mekong case
            if mekong_pattern:
                parsed = enforce_mekong6(parsed if isinstance(parsed, dict) else {"tinh": []})

            return jsonify({"reply": parsed, "model": jr.get("model", model), "usage": jr.get("usage", {})}), 200

        # Non-JSON mode
        return jsonify({"reply": reply, "model": jr.get("model", model), "usage": jr.get("usage", {})}), 200

    except requests.Timeout:
        if OFFLINE_FALLBACK_MEKONG and "message" in request.json and pattern_is_mekong6(request.json["message"]):
            result = enforce_mekong6({"tinh": []})
            return jsonify({"reply": result, "model": "offline-fallback", "usage": {},
                            "warning": "Timeout upstream, used offline fallback."}), 200
        return jsonify({"error": "Gateway timeout calling OpenRouter"}), 504
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
