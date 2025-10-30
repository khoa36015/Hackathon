from flask import Flask, jsonify
from data1 import dulieu
import random

app = Flask(__name__)

@app.route("/api/random-provinces", methods=["GET"])
def random_provinces():
    province_keys = list(dulieu.keys())

    # Random 6 tỉnh khác nhau
    selected = random.sample(province_keys, 6)

    # Gán ID từ 1 đến 6 và định dạng JSON theo yêu cầu
    provinces = {}
    for i, key in enumerate(selected, start=1):
        provinces[str(i)] = {
            "tinh": key,
            "data": dulieu[key]
        }

    return jsonify({
        "total": 6,
        "provinces": provinces
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
