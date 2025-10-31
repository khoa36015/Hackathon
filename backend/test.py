from flask import Flask, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)
 

@app.route("/api/itinerary/mine", methods=["GET"])
def get_my_itineraries():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    data = read_data()
    user_itineraries = [i for i in data if i["user_id"] == user_id]
    return jsonify({"itineraries": user_itineraries}), 200


@app.route("/api/itinerary/<id>", methods=["GET"])
def get_itinerary_delltail(id):
    data = read_data()
    for item in data:
        if item["id"] == id:
            return jsonify(item), 200
    return jsonify({"error": "Itinerary not found"}), 404 