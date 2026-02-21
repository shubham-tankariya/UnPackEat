import re

_JUNK_PATTERNS = re.compile(
    r"do not buy|keep away|marketed by|survey no|anc no|allergen advice|"
    r"^open$|^[0-9]+$|foundamaged|direct sunlight",
    re.IGNORECASE,
)

def _is_junk(item):
    """Return True if an ingredient entry looks like packaging text or OCR noise."""
    text = (item.get("text") or "").strip()
    if _JUNK_PATTERNS.search(text):
        return True
    if item.get("is_in_taxonomy") == 0 and item.get("percent_estimate", 1) == 0 and len(text) > 30:
        return True
    return False

def normalize_ingredient(item):
    return {
        "id":                   item.get("id"),
        "text":                 item.get("text"),
        "percent_estimate":     item.get("percent_estimate"),
        "percent_min":          item.get("percent_min"),
        "percent_max":          item.get("percent_max"),
        "vegan":                item.get("vegan"),
        "vegetarian":           item.get("vegetarian"),
        "ciqual_proxy_food_code": item.get("ciqual_proxy_food_code"),
        "ciqual_food_code":     item.get("ciqual_food_code"),
        "ecobalyse_code":       item.get("ecobalyse_code"),
        "from_palm_oil":        item.get("from_palm_oil"),
        "is_in_taxonomy":       item.get("is_in_taxonomy"),
    }

def is_additive(item):
    idv = item.get("id") or ""
    return bool(re.match(r"en:e\d+", idv.lower()))

def normalize(extracted):

    raw_ing = extracted["ingredients_raw"]["structured"]

    ingredients = []
    additives_from_ingredients = []

    for ing in raw_ing:
        if _is_junk(ing):
            continue
        n = normalize_ingredient(ing)
        if is_additive(ing):
            additives_from_ingredients.append(n)
        else:
            ingredients.append(n)

    additives_raw = extracted.get("additives_raw") or []

    if additives_raw:
        uniq = {}
        for tag in additives_raw:
            entry = {
                "id":                   tag,
                "text":                 tag.replace("en:", "").upper(),
                "percent_estimate":     None,
                "percent_min":          None,
                "percent_max":          None,
                "vegan":                None,
                "vegetarian":           None,
                "ciqual_proxy_food_code": None,
                "ciqual_food_code":     None,
                "ecobalyse_code":       None,
                "from_palm_oil":        None,
                "is_in_taxonomy":       None,
            }
            for a in additives_from_ingredients:
                if (a.get("id") or "").lower() == tag.lower():
                    entry.update({k: v for k, v in a.items() if v is not None})
                    break
            code = tag.replace("en:", "").upper()
            if code not in uniq:
                uniq[code] = entry
        additives = list(uniq.values())
    else:
        uniq = {}
        for a in additives_from_ingredients:
            code = (a["id"] or "").replace("en:", "").upper()
            if code not in uniq:
                uniq[code] = a
        additives = list(uniq.values())

    contains_palm_oil = any(
        (i.get("from_palm_oil") or "") in ("yes", "maybe")
        or "palm" in (i.get("id") or "")
        or "palm" in (i.get("text") or "").lower()
        for i in raw_ing
    )

    seen_text = set()
    dom = []
    for ing in raw_ing:
        if _is_junk(ing):
            continue
        if is_additive(ing):
            continue
        text = (ing.get("text") or "").strip()
        if not text or text in seen_text:
            continue
        pct = ing.get("percent_estimate") or 0
        if pct > 0:
            seen_text.add(text)
            dom.append({"ingredient": text, "percent": round(pct, 1)})
    dom = sorted(dom, key=lambda x: x["percent"], reverse=True)[:4]

    return {
        "product":   extracted["product"],
        "nutrients": extracted["nutrients"],
        "ingredients": {
            "text":             extracted["ingredients_raw"]["text"],
            "ingredients":      ingredients,
            "additives":        additives,
            "dominant":         dom,
            "contains_palm_oil": contains_palm_oil,
            "total_count":      len(ingredients),
        },
        "allergens": extracted["allergens_raw"],
        "serving":   extracted["serving"],
        "metadata":  extracted["metadata"],
    }
