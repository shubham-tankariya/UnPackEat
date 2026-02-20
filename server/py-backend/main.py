# main.py

import json
import os

from fastapi import FastAPI
from services.fetcher import fetch_product_from_api
from services.extractor import extract_product_data
from services.normalizer import normalize
from services.analyzer import analyze
from services.formatter import format_response

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Food Analyzer running"}

@app.get("/product/{barcode}")
async def get_product(barcode: str, debug: bool = False):

    raw = await fetch_product_from_api(barcode)
    extracted = extract_product_data(raw)
    normalized = normalize(extracted)
    analyzed = analyze(normalized)

    final = format_response(normalized, analyzed)

    # Always save structured response
    os.makedirs("data", exist_ok=True)
    with open(f"data/{barcode}.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2)

    # In debug mode, also save the raw OpenFoodFacts response
    if debug:
        os.makedirs("data/raw", exist_ok=True)
        with open(f"data/raw/{barcode}.json", "w", encoding="utf-8") as f:
            json.dump(raw, f, indent=2)

    return final


# --- Cached products in data/ ---
# 3017620422003
# 4008400402222
# 5000112548167
# 5000159484695
# 5449000000996
# 5449000131805
# 7622210449283
# 8901058023800
# 8901063367319
# 8901262130325
# 8901595971220
# 8901719130144
# 8903363001092
# 8903363006820
# 8904004400779
# 8904109490538
# 8906010500047
# 8906010500139
# 8906010500207
# 8906010500320
# 8906010500511
# 8906010501570
# 8906010503574
# 8906010505028
# 8906010505196
# 8906010505202
# 8906010505219
# 8906010505509
# 8908005144632