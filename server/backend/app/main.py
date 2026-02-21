from fastapi import FastAPI
from services.fetcher import fetch_product_from_api
from services.extractor import extract_product_data
from services.analyzer import analyze_product

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Food Analyzer running"}

@app.get("/product/{barcode}")
async def get_product(barcode: str, debug: bool = False):

    raw_product = await fetch_product_from_api(barcode)

    structured_data = extract_product_data(raw_product)

    analysis = analyze_product(structured_data)

    public_details = structured_data.copy()

    # Remove heavy nested ingredient list
    public_details["ingredients"] = {
        "ingredients_text": structured_data["ingredients"]["ingredients_text"],
        "total_count": structured_data["ingredients"]["total_count"],
        "additives_count": structured_data["ingredients"]["additives_count"],
        "contains_palm_oil": structured_data["ingredients"]["contains_palm_oil"],
        "decoded_additives": structured_data["ingredients"]["decoded_additives"],
    }

    response = {
        "summary": analysis,
        "details": public_details
    }


    if debug:
        return raw_product

    return response


# To test barcodes

# Everest
# 8901786060504

# Crunchex
# 8906010501570

# Chataka Pataka
# 8906010500511
