def analyze_product(data: dict):

    nutrition = data["nutrition"]
    meta = data["meta"]
    ingredients = data["ingredients"]

    score = 50
    risk_flags = []
    positives = []

    if nutrition["saturated_fat"] > 5:
        score -= 10
        risk_flags.append("High saturated fat")

    if nutrition["sugars"] > 10:
        score -= 8
        risk_flags.append("High sugar")

    if nutrition["salt"] > 1:
        score -= 8
        risk_flags.append("High salt")

    if meta["nova_group"] == 4:
        score -= 10
        risk_flags.append("Ultra-processed food")

    if ingredients["additives_count"] > 5:
        score -= 5
        risk_flags.append("High number of additives")

    if nutrition["fiber"] > 5:
        score += 8
        positives.append("High fiber")

    if nutrition["protein"] > 10:
        score += 5
        positives.append("Good protein content")

    score = max(0, min(score, 100))

    verdict = (
        "Healthy choice" if score >= 70
        else "Moderate consumption recommended" if score >= 40
        else "Limit consumption"
    )

    warnings = []

    if ingredients["contains_palm_oil"]:
        warnings.append("Contains palm oil")

    if meta.get("allergens_detected"):
        warnings.append("Contains allergens: " + ", ".join(meta["allergens_detected"]))


    return {
        "health_score": score,
        "verdict": verdict,
        "risk_flags": risk_flags,
        "positives": positives,
        "warnings": warnings,
        "nova_group": meta["nova_group"],
        "additives_count": ingredients["additives_count"]
    }
