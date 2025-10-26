from flask import Flask, jsonify
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)
CORS(app)
# them cors header
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp
# tao dieu huong cho api
@app.route('/api/ai/get-information-mientay', methods=['GET'])
def info_mientay():
    try:
        # goi api goc
        mientay_api = 'http://localhost:8000/api/ai/agent'
        payload = {'message': 'generate 6 tỉnh miền tây nổi bật random'}
        r = requests.post(mientay_api, json=payload, timeout=10)
        r.raise_for_status()
        data = r.json()
        # loc du lieu va chuyen du lieu ve array sau do chuyen nguoc lai json
        tinh = (data.get("reply") or {}).get("tinh", [])
        if not isinstance(tinh, list):
            tinh = []
        MEKONG_PROVINCES = [
            "an giang", "bac lieu", "ben tre", "ca mau", "can tho", "dong thap",
            "hau giang", "kien giang", "long an", "soc trang", "tien giang", "tra vinh",
            "vinh long"]
        result = []
        for t in tinh:
            if t in MEKONG_PROVINCES:
                result.append(t)
        return add_cors_headers(jsonify(result)), 200
    except requests.exceptions.RequestException as e:
        return add_cors_headers(jsonify({"status": "error", "error": str(e)})), 502
if __name__ == '__main__':
    app.run(port=40, debug=True)
