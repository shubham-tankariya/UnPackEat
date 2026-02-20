import httpx
from fastapi import HTTPException

OPENFOODFACTS_URL = "https://world.openfoodfacts.net/api/v2/product/"

async def fetch_product_from_api(barcode: str):
    url = f"{OPENFOODFACTS_URL}{barcode}"

    async with httpx.AsyncClient(timeout=6.0) as client:
        res = await client.get(url)

        data = res.json()

        return data["product"]