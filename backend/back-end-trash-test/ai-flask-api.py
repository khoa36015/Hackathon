import os
import json
import re
import unicodedata
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
REFERER = os.getenv("OPENROUTER_HTTP_REFERER", "")
X_TITLE = os.getenv("OPENROUTER_X_TITLE", "Local Dev Agent")

if not OPENROUTER_API_KEY:
    print("[WARN] Missing OPENROUTER_API_KEY in .env — /api/ai/agent calls will fail upstream.")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ALLOW_ORIGINS}})

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


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
    """Extract JSON object from a string; strip fences and cut from first { to last }."""
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


# ====== Route (UNCHANGED: /api/ai/agent) ======
@app.route("/api/ai/agent", methods=["POST"])
def ai_agent():
    """
    Accept JSON:
    {
      "message": "text",
      "history": [{"role":"user","content":"..."}, {"role":"assistant","content":"..."}],
      "model": "openai/gpt-4o-mini",
      "system": "override system prompt",
      "temperature": 0.7,
      "max_tokens": 512,

      // NEW (optional, no endpoint/port change):
      "json_mode": true,
      "json_schema": {...},                   // JSON Schema to enforce
      "postprocess": {"array_string_keys": ["tinh"]}  // lowercase/no-diacritics
    }
    Returns JSON:
    { "reply": <object|string>, "model": "...", "usage": {...} }
    """
    try:
        data = request.get_json(force=True, silent=False) or {}
        message = (data.get("message") or "").strip()
        if not message:
            return jsonify({"error": "Missing 'message'"}), 400

        model = (data.get("model") or DEFAULT_MODEL).strip()
        system_override = data.get("system")
        history = data.get("history")
        temperature = data.get("temperature", 0.7)
        max_tokens = data.get("max_tokens", None)

        json_mode = bool(data.get("json_mode", False))
        json_schema = data.get("json_schema")
        postprocess_cfg = data.get("postprocess") or {}
        array_string_keys = postprocess_cfg.get("array_string_keys", [])

        # If the user asks for 6 Mekong provinces, auto-enable strict JSON with schema
        auto_schema = None
        lower_msg = message.lower()
        if ("6" in lower_msg or "sáu" in lower_msg or "sau " in lower_msg) and ("miền tây" in lower_msg or "mien tay" in lower_msg):
            json_mode = True
            auto_schema = {
                "type": "object",
                "properties": {
                    "tinh": {
                        "type": "array",
                        "items": {"type": "string", "pattern": "^[a-z ]+$"},
                        "minItems": 6, "maxItems": 6, "uniqueItems": True
                    }
                },
                "required": ["tinh"],
                "additionalProperties": False
            }
            # Force a strict system prompt to forbid extra words
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

        # Enforce JSON format
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

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        if REFERER: headers["HTTP-Referer"] = REFERER
        if X_TITLE: headers["X-Title"] = X_TITLE

        resp = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=60)
        if resp.status_code >= 400:
            try:
                err = resp.json()
            except Exception:
                err = {"message": resp.text}
            return jsonify({"error": "OpenRouter error", "details": err}), resp.status_code

        jr = resp.json()
        choice = (jr.get("choices") or [{}])[0]
        reply = (choice.get("message") or {}).get("content", "")

        if json_mode or auto_schema:
            parsed = parse_json_strict(reply)
            if parsed is None:
                return jsonify({"error": "Invalid JSON from model", "raw": reply}), 502
            parsed = transform_array_strings(parsed, array_string_keys or (["tinh"] if auto_schema else []))
            return jsonify({"reply": parsed, "model": jr.get("model", model), "usage": jr.get("usage", {})}), 200

        # Non-JSON mode: return raw string
        return jsonify({
            "reply": reply,
            "model": jr.get("model", model),
            "usage": jr.get("usage", {}),
        }), 200

    except requests.Timeout:
        return jsonify({"error": "Gateway timeout calling OpenRouter"}), 504
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


if __name__ == "__main__":
    # Keep SAME port behavior: uses env PORT (default 8000)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
