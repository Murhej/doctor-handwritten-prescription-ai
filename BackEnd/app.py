from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # ✅ THIS FIXES CORS

@app.route("/", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # TODO: replace with real model logic
    return jsonify({
        "prediction": "Paracetamol",
        "confidence": 0.94
    })

@app.route("/medicine/<drug>", methods=["GET"])
def medicine(drug):
    return jsonify({
        "safety_info": {
            "usage": "Pain relief",
            "warnings": "Do not exceed recommended dose"
        }
    })

if __name__ == "__main__":
    app.run()
