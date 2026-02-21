import json
import os
from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from services.fetcher import fetch_product_from_api
from services.extractor import extract_product_data
from services.normalizer import normalize
from services.analyzer import analyze
from services.formatter import format_response
from services.ai_insights import generate_insights

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
    insights = generate_insights(normalized, analyzed)

    final = format_response(normalized, analyzed, ai_insights=insights)

    return final