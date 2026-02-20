# extractor.py

import re

def safe_float(x):
    try:
        return float(x)
    except:
        return None

def extract_serving_size(serving_raw: str):
    if not serving_raw:
        return None
    match = re.search(r"(\d+\.?\d*)\s*g", serving_raw.lower())
    return float(match.group(1)) if match else None

def flatten_ingredients(ingredients):
    flat = []

    def walk(items):
        for ing in items:
            flat.append(ing)
            if isinstance(ing.get("ingredients"), list):
                walk(ing["ingredients"])

    walk(ingredients or [])
    return flat

COMMON_ALLERGENS = [
    "milk", "lactose",
    "soy", "soya",
    "egg",
    "wheat", "gluten",
    "almond", "cashew", "peanut", "groundnut",
    "sesame", "mustard", "hazelnut"
]

def detect_allergens(text, traces, tags):
    text = (text or "").lower()
    detected = set()

    for a in COMMON_ALLERGENS:
        if a in text or any(a in t for t in traces):
            detected.add(a)

    for tag in tags:
        clean = tag.replace("en:", "")
        detected.add(clean)

    return list(sorted(detected))


def extract_product_data(raw: dict):

    nutr = raw.get("nutriments") or {}

    nutrients = {
        "energy_kcal": safe_float(nutr.get("energy-kcal") or nutr.get("energy-kcal_100g")),
        "fat": safe_float(nutr.get("fat")),
        "saturated_fat": safe_float(nutr.get("saturated-fat")),
        "carbohydrates": safe_float(nutr.get("carbohydrates")),
        "sugars": safe_float(nutr.get("sugars")),
        "fiber": safe_float(nutr.get("fiber")),
        "protein": safe_float(nutr.get("proteins")),
        "salt": safe_float(nutr.get("salt")),
    }

    ing_list = raw.get("ingredients") or []
    flattened = flatten_ingredients(ing_list)

    additives_raw = raw.get("additives_tags") or []

    serving_raw = raw.get("serving_size")
    serving_g = extract_serving_size(serving_raw)

    allergens = detect_allergens(
        raw.get("ingredients_text"),
        raw.get("traces_tags") or [],
        raw.get("allergens_tags") or []
    )

    return {
        "product": {
            "code": raw.get("code"),
            "name": raw.get("product_name") or "Unknown",
            "brand": raw.get("brands") or "Unknown",
            "image": raw.get("image_url"),
            "quantity": raw.get("quantity"),
            "categories": raw.get("categories_tags") or [],
        },
        "nutrients": nutrients,
        "ingredients_raw": {
            "text": raw.get("ingredients_text") or "",
            "structured": flattened,
        },
        "additives_raw": additives_raw,
        "allergens_raw": allergens,
        "serving": {
            "serving_size": serving_raw,
            "serving_size_g": serving_g,
        },
        "metadata": {
            "nova_group": raw.get("nova_group"),
            "ecoscore": raw.get("ecoscore_grade"),
            "packaging": raw.get("packaging_materials_tags") or [],
        }
    }
