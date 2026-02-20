from fastapi import FastAPI
from services.fetcher import fetch_product_from_api

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Food Analyzer running"}

@app.get("/product/{barcode}")
async def get_product(barcode: str, debug: bool = False):

    product = await fetch_product_from_api(barcode)

    return product