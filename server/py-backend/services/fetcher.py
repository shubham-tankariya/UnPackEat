import httpx
from fastapi import HTTPException

OPENFOODFACTS_URL = "https://world.openfoodfacts.net/api/v2/product/"


async def fetch_product_from_api(barcode: str):
    url = f"{OPENFOODFACTS_URL}{barcode}"

    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            res = await client.get(url)
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Unable to reach OpenFoodFacts")

    if res.status_code == 404:
        raise HTTPException(status_code=404, detail="Product not found")

    if res.status_code != 200:
        raise HTTPException(status_code=502, detail="OpenFoodFacts API error")

    try:
        data = res.json()
    except ValueError:
        raise HTTPException(status_code=502, detail="Invalid OpenFoodFacts response")

    if data.get("status") == 0:
        raise HTTPException(status_code=404, detail=data.get("status_verbose", "Product not found"))

    product = data.get("product")
    if not product:
        raise HTTPException(status_code=502, detail="Malformed product response")

    return product
