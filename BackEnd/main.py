from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from predict import predict_image_bytes
import json
import os

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load medicine safety database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "medicine_data.json"), "r", encoding="utf-8") as f:
    MEDICINE_DB = json.load(f)

@app.get("/")
def home():
    return {"status": "CRNN Backend Running ✅"}

# ✅ OCR PREDICTION ROUTE (UNCHANGED)
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = predict_image_bytes(image_bytes)
    return result

@app.get("/medicine/{name}")
def get_medicine_info(name: str):
    key = name.strip()

    # ✅ Direct match
    if key in MEDICINE_DB:
        return {
            "medicine": key,
            "safety_info": MEDICINE_DB[key]
        }

    # ✅ Brand → Generic conversion
    if "_brand_to_generic" in MEDICINE_DB:
        brand_map = MEDICINE_DB["_brand_to_generic"]
        if key in brand_map:
            generic = brand_map[key]
            return {
                "medicine": generic,
                "safety_info": MEDICINE_DB[generic]
            }

    # ✅ Case-insensitive fallback
    for med in MEDICINE_DB:
        if med.lower() == key.lower():
            return {
                "medicine": med,
                "safety_info": MEDICINE_DB[med]
            }

    return {"error": "Medicine not found"}
