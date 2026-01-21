from flask import Flask, jsonify
import os
import json

app = Flask(__name__)   # 🔴 THIS WAS MISSING

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "brand_to_generic.json"), "r", encoding="utf-8") as f:
    brand_map = json.load(f)

with open(os.path.join(BASE_DIR, "medicine_data.json"), "r", encoding="utf-8") as f:
    medicine_info = json.load(f)

@app.route("/")
def health():
    return {"status": "Doctor Prescription AI running"}

@app.route("/drug/<name>")
def get_drug(name):
    generic = brand_map.get(name)
    if not generic:
        return jsonify({"error": "Brand not found"}), 404
    return jsonify(medicine_info.get(generic, {"error": "Generic info missing"}))
