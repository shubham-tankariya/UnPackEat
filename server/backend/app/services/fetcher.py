import httpx
from fastapi import HTTPException

OPENFOODFACTS_URL = "https://world.openfoodfacts.net/api/v2/product/"

async def fetch_product_from_api(barcode: str):

    url = f"{OPENFOODFACTS_URL}{barcode}"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to OpenFoodFacts"
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="OpenFoodFacts API error"
        )

# Parsing
    try:
        data = response.json()
    except ValueError:
        raise HTTPException(
            status_code=502,
            detail="Invalid response from OpenFoodFacts"
        )

    # Handle status field if present
    if data.get("status") == 0:
        raise HTTPException(
            status_code=404,
            detail=data.get("status_verbose", "Product not found")
        )

    if "product" not in data:
        raise HTTPException(
            status_code=502,
            detail="Malformed product response"
        )

    return data["product"]
