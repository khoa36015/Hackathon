from flask import Flask, jsonify
import requests
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*" 
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
        r.raise_for_status() 

        data = r.json() 

        response = jsonify({
            "status": "success",
            "source": mientay_api,
            "data": data
        })
        return add_cors_headers(response)

    except requests.exceptions.RequestException as e:

        response = jsonify({
            "status": "error",
            "error": str(e)
        })
        return add_cors_headers(response), 502


if __name__ == '__main__':
    app.run(port=5000, debug=True)
