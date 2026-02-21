def analyze_product(data: dict):

    nutrition = data["nutrition"]
    meta = data["meta"]
    ingredients = data["ingredients"]

    energy = nutrition["energy_kcal"]
    fat = nutrition["fat"]
    carbs = nutrition["carbohydrates"]
    protein = nutrition["protein"]

    # Avoid division by zero
    macro_percent = {}
    if energy > 0:
        macro_percent = {
            "fat_percent_calories": round((fat * 9 / energy) * 100, 1),
            "carb_percent_calories": round((carbs * 4 / energy) * 100, 1),
            "protein_percent_calories": round((protein * 4 / energy) * 100, 1),
        }

    daily_context = []

    if nutrition["saturated_fat"] > 0:
        daily_context.append(
            f"Saturated fat: {nutrition['saturated_fat']}g per 100g "
            "(recommended limit ~20g/day)"
        )

    if nutrition["salt"] > 0:
        daily_context.append(
            f"Salt: {nutrition['salt']}g per 100g "
            "(recommended limit ~5g/day)"
        )

    portion_info = None
    quantity = data["basic_info"]["quantity"]

    try:
        if quantity and "g" in quantity.lower():
            pack_weight = float(quantity.lower().replace("g", "").strip())
            portion_info = {
                "calories_per_pack": round((energy * pack_weight) / 100, 1)
            }
    except:
        portion_info = None


    score = 50
    risk_flags = []
    positives = []
    score_breakdown = []

    if nutrition["saturated_fat"] > 5:
        score -= 10
        risk_flags.append("High saturated fat")
        score_breakdown.append({
            "reason": "High saturated fat",
            "impact": -10,
            "value": nutrition["saturated_fat"],
            "threshold": "> 5g per 100g"
        })

    if nutrition["sugars"] > 10:
        score -= 8
        risk_flags.append("High sugar")
        score_breakdown.append({
            "reason": "High sugar",
            "impact": -8,
            "value": nutrition["sugars"],
            "threshold": "> 10g per 100g"
        })

    if nutrition["salt"] > 1:
        score -= 8
        risk_flags.append("High salt")
        score_breakdown.append({
            "reason": "High salt",
            "impact": -8,
            "value": nutrition["salt"],
            "threshold": "> 1g per 100g"
        })

    if meta["nova_group"] == 4:
        score -= 10
        risk_flags.append("Ultra-processed food")
        score_breakdown.append({
            "reason": "Ultra-processed (NOVA 4)",
            "impact": -10,
            "value": meta["nova_group"],
            "threshold": "NOVA group 4"
        })

    if ingredients["additives_count"] > 5:
        score -= 5
        risk_flags.append("High number of additives")
        score_breakdown.append({
            "reason": "Multiple additives",
            "impact": -5,
            "value": ingredients["additives_count"],
            "threshold": "> 5 additives"
        })

    if nutrition["fiber"] > 5:
        score += 8
        positives.append("High fiber")
        score_breakdown.append({
            "reason": "High fiber",
            "impact": +8,
            "value": nutrition["fiber"],
            "threshold": "> 5g per 100g"
        })

    if nutrition["protein"] > 10:
        score += 5
        positives.append("Good protein content")
        score_breakdown.append({
            "reason": "Good protein content",
            "impact": +5,
            "value": nutrition["protein"],
            "threshold": "> 10g per 100g"
        })

    score = max(0, min(score, 100))

    long_term_risks = []

    if nutrition["saturated_fat"] > 5:
        long_term_risks.append("Frequent high saturated fat intake is linked to heart disease risk.")

    if nutrition["salt"] > 1:
        long_term_risks.append("High salt intake may increase blood pressure risk.")

    if nutrition["sugars"] > 10:
        long_term_risks.append("High sugar consumption may increase metabolic risk.")

    if meta["nova_group"] == 4:
        long_term_risks.append("Ultra-processed foods are associated with long-term metabolic risks.")


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

    complexity_index = "Simple formulation"

    if ingredients["total_count"] > 20:
        complexity_index = "Highly complex formulation"
    elif ingredients["total_count"] > 10:
        complexity_index = "Moderately complex formulation"


    return {
        "health_score": score,
        "verdict": verdict,
        "risk_flags": risk_flags,
        "positives": positives,
        "warnings": warnings,
        "nova_group": meta["nova_group"],
        "additives_count": ingredients["additives_count"],
        "macro_percent_distribution": macro_percent,
        "daily_context": daily_context,
        "portion_insight": portion_info,
        "score_breakdown": score_breakdown,
        "long_term_risk_hints": long_term_risks,
        "ingredient_complexity": complexity_index
    }
    