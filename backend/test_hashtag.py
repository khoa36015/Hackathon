#hashtag bao gồm:#am_thuc,#bien,#tam_linh,#kham_pha,#thien_nhien,#lich_su,#van_hoa,#giai_tri
from flask import Flask, jsonify, request
from data import data

app = Flask(__name__)

@app.route("/api/search_by_hashtag/<tag>", methods=["GET"])
def search_by_hashtag(tag):
    tag = "#" + tag.lower()  # thêm # để khớp hashtag
    results = [item for item in data if tag in [t.lower() for t in item["hashtags"]]]
    return jsonify(results), 200

if __name__ == "__main__":
    app.run(debug=True)
