from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from predict import predict_image_bytes
import json
import os
import urllib.parse

app = FastAPI()

# 🔓 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 📦 Load medicine database
with open(os.path.join(BASE_DIR, "medicine_data.json"), "r", encoding="utf-8") as f:
    MEDICINE_DB = json.load(f)

BRAND_MAP = MEDICINE_DB.get("_brand_to_generic", {})

@app.get("/")
def home():
    return {"status": "CRNN Backend Running ✅"}

# 🧠 OCR
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return predict_image_bytes(image_bytes)

# 💊 Medicine lookup
@app.get("/medicine/{name}")
def get_medicine_info(name: str):
    key = urllib.parse.unquote(name).strip()

    # 1️⃣ Exact generic
    if key in MEDICINE_DB and key != "_brand_to_generic":
        return {
            "medicine": key,
            "brand": None,
            "safety_info": MEDICINE_DB[key],
        }

    # 2️⃣ Brand → Generic
    if key in BRAND_MAP:
        generic = BRAND_MAP[key]
        return {
            "medicine": generic,
            "brand": key,
            "safety_info": MEDICINE_DB.get(generic),
        }

    # 3️⃣ Case-insensitive fallback
    for med in MEDICINE_DB:
        if med.lower() == key.lower():
            return {
                "medicine": med,
                "brand": None,
                "safety_info": MEDICINE_DB[med],
            }

    return {"error": "Medicine not found"}
