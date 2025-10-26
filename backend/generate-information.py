from flask import Flask, jsonify
import requests
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # tự động bật CORS cho toàn bộ API

def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"  # hoặc "http://127.0.0.1:5500" nếu cần chính xác
    resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp


@app.route('/api/ai/get-information-mientay', methods=['GET'])
def info_mientay():
    try:
        mientay_api = 'http://localhost:8000/api/ai/agent'
        payload = {'message': 'generate 6 tỉnh miền tây nổi bật random'}

       
        r = requests.post(mientay_api, json=payload, timeout=10)
        r.raise_for_status()  # nếu lỗi HTTP (400–500) sẽ ném exception

        data = r.json()  # parse JSON trả về

        response = jsonify({
            "status": "success",
            "source": mientay_api,
            "data": data
        })
        return add_cors_headers(response)

    except requests.exceptions.RequestException as e:
        # Nếu API kia không chạy hoặc timeout
        response = jsonify({
            "status": "error",
            "error": str(e)
        })
        return add_cors_headers(response), 502


if __name__ == '__main__':
    app.run(port=5000, debug=True)
