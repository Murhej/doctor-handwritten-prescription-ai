import os
import json
from flask import Flask, request, jsonify

# -------------------
# Flask app (REQUIRED)
# -------------------
app = Flask(__name__)

# -------------------
# Load data files
# -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "brand_to_generic.json"), "r", encoding="utf-8") as f:
    brand_map = json.load(f)

with open(os.path.join(BASE_DIR, "medicine_data.json"), "r", encoding="utf-8") as f:
    medicine_info = json.load(f)

# -------------------
# Logic function
# -------------------
def get_drug_info(ocr_prediction):
    generic = brand_map.get(ocr_prediction)

    if not generic:
        return {"error": "Brand not found"}

    return medicine_info.get(generic, {"error": "Generic info missing"})

# -------------------
# API endpoint
# -------------------
@app.route("/drug-info", methods=["POST"])
def drug_info():
    data = request.get_json()
    ocr_prediction = data.get("prediction")

    if not ocr_prediction:
        return jsonify({"error": "Missing prediction"}), 400

    result = get_drug_info(ocr_prediction)
    return jsonify(result)

# -------------------
# Health check
# -------------------
@app.route("/")
def home():
    return "Handwritten Prescription API is running"
