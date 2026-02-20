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
    "sesame", "mustard", "hazelnut", "tree nut"
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

    return sorted(detected)


def _nutriment(nutr, key):
    """
    Pull a nutriment value from the nutriments dict.
    Tries key, then key_100g (in case the product is reported per-serving).
    """
    return safe_float(nutr.get(key) or nutr.get(f"{key}_100g"))


def extract_product_data(raw: dict):

    nutr = raw.get("nutriments") or {}
    nutrition_data_per = raw.get("nutrition_data_per", "100g")

    raw_salt   = _nutriment(nutr, "salt")
    raw_sodium = _nutriment(nutr, "sodium")
    if raw_salt is None and raw_sodium is not None:
        raw_salt = round(raw_sodium * 2.5, 4)

    nutrients = {
        "energy_kcal":   _nutriment(nutr, "energy-kcal"),
        "fat":           _nutriment(nutr, "fat"),
        "saturated_fat": _nutriment(nutr, "saturated-fat"),
        "carbohydrates": _nutriment(nutr, "carbohydrates"),
        "sugars":        _nutriment(nutr, "sugars"),
        "fiber":         _nutriment(nutr, "fiber"),
        "protein":       _nutriment(nutr, "proteins"),
        "salt":          raw_salt,
        "cholesterol":   _nutriment(nutr, "cholesterol"),
    }

    ing_list  = raw.get("ingredients") or []
    flattened = flatten_ingredients(ing_list)

    additives_raw = raw.get("additives_tags") or []

    serving_raw = raw.get("serving_size")
    serving_g   = extract_serving_size(serving_raw)

    allergens = detect_allergens(
        raw.get("ingredients_text"),
        raw.get("traces_tags") or [],
        raw.get("allergens_tags") or []
    )

    nutriscore_obj = raw.get("nutriscore") or {}
    nutriscore_grade = (
        nutriscore_obj.get("2023", {}).get("grade")
        or nutriscore_obj.get("2021", {}).get("grade")
        or raw.get("nutriscore_grade")
    )

    if nutriscore_grade in ("unknown", "not-applicable", "not_applicable"):
        nutriscore_grade = None

    labels_tags = raw.get("labels_tags") or []

    off_completeness     = safe_float(raw.get("completeness"))
    data_quality_warnings = raw.get("data_quality_warnings_tags") or []

    nutrient_levels = raw.get("nutrient_levels") or {} 

    food_groups     = (raw.get("food_groups_tags") or [])
    countries_tags  = raw.get("countries_tags") or []
    nova_group_error = raw.get("nova_group_error")

    return {
        "product": {
            "code":       raw.get("code"),
            "name":       raw.get("product_name") or "Unknown",
            "brand":      raw.get("brands") or "Unknown",
            "image":      raw.get("image_url"),
            "quantity":   raw.get("quantity"),
            "categories": raw.get("categories_tags") or [],
        },
        "nutrients": nutrients,
        "ingredients_raw": {
            "text":       raw.get("ingredients_text") or "",
            "structured": flattened,
        },
        "additives_raw":   additives_raw,
        "allergens_raw":   allergens,
        "serving": {
            "serving_size":       serving_raw,
            "serving_size_g":     serving_g,
            "nutrition_data_per": nutrition_data_per,
        },
        "metadata": {
            "nova_group":          raw.get("nova_group"),
            "nova_group_error":    nova_group_error,
            "nutriscore_grade":    nutriscore_grade,
            "nutrient_levels":     nutrient_levels,
            "ecoscore":            raw.get("ecoscore_grade"),
            "packaging":           raw.get("packaging_materials_tags") or [],
            "labels":              labels_tags,
            "off_completeness":    off_completeness,
            "data_quality_warnings": data_quality_warnings,
            "food_groups":         food_groups,
            "countries":           countries_tags,
        }
    }
