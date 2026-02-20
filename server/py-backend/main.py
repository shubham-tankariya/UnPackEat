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

    product = await fetch_product_from_api(barcode)
    structured_data = extract_product_data(product)
    analysis = analyze_product(structured_data)

    response = {
        "summary": analysis,
        "details": structured_data
    }

    return response