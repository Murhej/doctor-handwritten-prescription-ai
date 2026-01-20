import json

with open("brand_to_generic.json") as f:
    brand_map = json.load(f)

with open("medicine_info.json") as f:
    medicine_info = json.load(f)

def get_drug_info(ocr_prediction):
    generic = brand_map.get(ocr_prediction)

    if not generic:
        return {"error": "Brand not found"}

    return medicine_info.get(generic, {"error": "Generic info missing"})
