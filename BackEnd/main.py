from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from predict import predict_image_bytes
import json
import os
import urllib.parse

app = FastAPI()

# ✅ CORS (safe for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load medicine database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "medicine_data.json"), "r", encoding="utf-8") as f:
    MEDICINE_DB = json.load(f)

@app.get("/")
def home():
    return {"status": "CRNN Backend Running ✅"}

# ✅ OCR prediction
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return predict_image_bytes(image_bytes)

# ✅ Medicine lookup (BRAND → GENERIC → SAFETY)
@app.get("/medicine/{name}")
def get_medicine_info(name: str):
    # Decode URL (%20, +, etc.)
    key = urllib.parse.unquote(name).strip()

    brand_map = MEDICINE_DB.get("_brand_to_generic", {})

    # 1️⃣ Direct generic match
    if key in MEDICINE_DB:
        return {
            "medicine": key,
            "brand": None,
            "safety_info": MEDICINE_DB[key],
        }

    # 2️⃣ Brand → Generic
    if key in brand_map:
        generic = brand_map[key]
        if generic in MEDICINE_DB:
            return {
                "medicine": generic,
                "brand": key,
                "safety_info": MEDICINE_DB[generic],
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
