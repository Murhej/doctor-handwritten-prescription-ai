import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "brand_to_generic.json"), "r", encoding="utf-8") as f:
    brand_map = json.load(f)

with open(os.path.join(BASE_DIR, "medicine_info.json"), "r", encoding="utf-8") as f:
    medicine_info = json.load(f)

def get_drug_info(ocr_prediction):
    generic = brand_map.get(ocr_prediction)

    if not generic:
        return {"error": "Brand not found"}

    return medicine_info.get(generic, {"error": "Generic info missing"})
