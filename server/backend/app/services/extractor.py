def extract_product_data(product: dict):

    nutriments = product.get("nutriments") or {}

    def safe_number(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0

    ingredients_text = (product.get("ingredients_text") or "").lower()
    traces = product.get("traces_tags") or []

    allergens_detected = set()

    if "milk" in ingredients_text or any("milk" in t for t in traces):
        allergens_detected.add("milk / lactose")

    if "groundnut" in ingredients_text or "peanut" in ingredients_text or any("peanut" in t for t in traces):
        allergens_detected.add("nuts")

    if "soya" in ingredients_text or "soy" in ingredients_text:
        allergens_detected.add("soy")

    if "wheat" in ingredients_text or "gluten" in ingredients_text:
        allergens_detected.add("gluten")


    return {
        "basic_info": {
            "name": product.get("product_name") or "Unknown",
            "brand": product.get("brands") or "Unknown",
            "quantity": product.get("quantity"),
            "image": product.get("image_url"),
            "category": product.get("categories"),
        },
        "nutrition": {
            "energy_kcal": safe_number(nutriments.get("energy-kcal")),
            "fat": safe_number(nutriments.get("fat")),
            "saturated_fat": safe_number(nutriments.get("saturated-fat")),
            "carbohydrates": safe_number(nutriments.get("carbohydrates")),
            "sugars": safe_number(nutriments.get("sugars")),
            "protein": safe_number(nutriments.get("proteins")),
            "fiber": safe_number(nutriments.get("fiber")),
            "salt": safe_number(nutriments.get("salt")),
        },
        "ingredients": {
            "list": product.get("ingredients") or [],
            "ingredients_text": product.get("ingredients_text") or "",
            "total_count": product.get("ingredients_n") or 0,
            "additives_count": product.get("additives_n") or 0,
            "decoded_additives": [
                {
                    "code": tag.replace("en:", "").upper(),
                    "type": "Flavour enhancer" if tag in ["en:e627", "en:e631"]
                    else "Acidity regulator" if tag in ["en:e330", "en:e296", "en:e334"]
                    else "Stabilizer" if tag == "en:e340"
                    else "Emulsifier" if tag == "en:e470"
                    else "Anti-caking agent" if tag == "en:e551"
                    else "Color" if tag == "en:e160c"
                    else "Food additive"
                }
                for tag in (product.get("additives_tags") or [])
            ],
            "contains_palm_oil": "en:palm-oil" in (product.get("ingredients_analysis_tags") or []),
            "dominant_ingredients": [f"{ing.get('text')} ({ing.get('percent')}%)" for ing in (product.get("ingredients") or [])if ing.get("percent")][:3],

        },
        "meta": {
            "nova_group": product.get("nova_group") or 0,
            "ecoscore_grade": product.get("ecoscore_grade") or "unknown",
            "packaging_materials": product.get("packaging_materials_tags") or [],
            "traces": product.get("traces_tags") or [],
            "allergens_detected": list(allergens_detected)
        }

    }
