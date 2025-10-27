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
        payload = {
            'message': 'Liệt kê 6 tỉnh miền tây theo định dạng array như sau ["tỉnh 1", "tỉnh 2",...]'
        }
        
        r = requests.post(mientay_api, json=payload, timeout=10)
        r.raise_for_status()
        
        # Log raw response for debugging
        print("Raw API Response:", r.text)
        
        data = r.json()
        print("Parsed Response:", json.dumps(data, indent=2))

        # Extract tinh from response with simpler validation
        tinh = []
        if isinstance(data, dict):
            if 'tinh' in data:  # Check for tinh directly in data
                tinh = data['tinh']
            elif 'reply' in data and isinstance(data['reply'], dict) and 'tinh' in data['reply']:
                tinh = data['reply']['tinh']

        print("Extracted provinces:", tinh)

        if not tinh:
            return add_cors_headers(jsonify({
                "status": "error", 
                "message": "No provinces data received",
                "raw_response": data
            })), 404

        MEKONG_PROVINCES = [
            "an giang", "bac lieu", "ben tre", "ca mau", "can tho", "dong thap",
            "hau giang", "kien giang", "long an", "soc trang", "tien giang", "tra vinh",
            "vinh long"
        ]
        
        result = []
        for idx, province in enumerate(tinh, 1):  #liet ke cac tinh danh index tu 1
            province_name = province.lower() if isinstance(province, str) else ""
            if province_name in MEKONG_PROVINCES:
                result.append({
                    "id": idx,
                    "province": province_name.title()
                })

        if not result:
            return add_cors_headers(jsonify({"status": "error", "message": "No valid Mekong provinces found"})), 404

        print("Final result:", result)
        return add_cors_headers(jsonify(result)), 200
        
    except requests.exceptions.RequestException as e:
        return add_cors_headers(jsonify({"status": "error", "error": str(e)})), 502
if __name__ == '__main__':
    app.run(port=40, debug=True)
