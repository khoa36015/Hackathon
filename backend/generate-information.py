from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
#them cors vao de khong bi loi cors
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1/"
    resp.headers["Vary"] = "Origin"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp

