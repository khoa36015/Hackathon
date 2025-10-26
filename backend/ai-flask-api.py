import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
#Chinh Sua Trong file .env
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openai/gpt-4o-mini")  
DEFAULT_SYSTEM = os.getenv("DEFAULT_SYSTEM", "You are a helpful assistant. Keep answers concise.")
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*")
REFERER = os.getenv("OPENROUTER_HTTP_REFERER", "")  
X_TITLE = os.getenv("OPENROUTER_X_TITLE", "Local Dev Agent")

if not OPENROUTER_API_KEY:
    raise RuntimeError("Missing OPENROUTER_API_KEY in .env")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ALLOW_ORIGINS}})

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def build_messages(user_message: str, system_override: str | None, history: list | None):
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
      "max_tokens": 512
    }
    Returns JSON:
    { "reply": "...", "model": "...", "usage": {...}, "raw": {...optional} }
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

        payload = {
            "model": model,
            "messages": build_messages(message, system_override, history),
            "temperature": temperature,
        }
        if isinstance(max_tokens, int) and max_tokens > 0:
            payload["max_tokens"] = max_tokens

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        if REFERER:
            headers["HTTP-Referer"] = REFERER
        if X_TITLE:
            headers["X-Title"] = X_TITLE

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

        return jsonify({
            "reply": reply,
            "model": jr.get("model", model),
            "usage": jr.get("usage", {}),
            # Comment this out in prod if you don't want to return the raw response
            # "raw": jr
        }), 200

    except requests.Timeout:
        return jsonify({"error": "Gateway timeout calling OpenRouter"}), 504
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
