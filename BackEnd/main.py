from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from BackEnd.predict import predict_image_bytes
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "medicine_data.json"), "r", encoding="utf-8") as f:
    MEDICINE_DB = json.load(f)

@app.get("/")
def home():
    return {"status": "CRNN Backend Running ✅"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = predict_image_bytes(image_bytes)
    return result

@app.get("/medicine/{name}")
def get_medicine_info(name: str):
    if name in MEDICINE_DB:
        return {"medicine": name, "safety_info": MEDICINE_DB[name]}
    return {"error": "Medicine not found"}
