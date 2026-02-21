def format_response(normalized, analyzed, ai_insights=None):

    meta = normalized["metadata"]

    return {
        "barcode":  normalized["product"]["code"],
        "product":  normalized["product"],
        "highlights": analyzed["highlights"],
        "nutrients":  analyzed["nutrients"],
        "nutrient_radar": analyzed["nutrient_radar"],
        "ingredients": {
            "text":             normalized["ingredients"]["text"],
            "ingredients":      normalized["ingredients"]["ingredients"],
            "additives":        normalized["ingredients"]["additives"],
            "dominant":         normalized["ingredients"]["dominant"],
            "contains_palm_oil": normalized["ingredients"]["contains_palm_oil"],
            "complexity": (
                "Highly complex"    if normalized["ingredients"]["total_count"] > 20 else
                "Moderately complex" if normalized["ingredients"]["total_count"] > 10 else
                "Simple formulation"
            )
        },
        "additives_full": analyzed["additives_full"],
        "allergens":  normalized["allergens"],
        "serving":    analyzed["serving"],
        "metadata": {
            "nova_group":       meta.get("nova_group"),
            "nova_group_error": meta.get("nova_group_error"),
            "nutriscore_grade": meta.get("nutriscore_grade"),
            "nutrient_levels":  meta.get("nutrient_levels"),
            "labels":           meta.get("labels"),
            "food_groups":      meta.get("food_groups"),
            "countries":        meta.get("countries"),
            "off_completeness": meta.get("off_completeness"),
            "data_quality_warnings": meta.get("data_quality_warnings"),
            "nutrition_data_per": normalized["serving"].get("nutrition_data_per"),
        },
        "environment": {
            "ecoscore":  meta.get("ecoscore"),
            "packaging": meta.get("packaging"),
        },
        "ai_insights": ai_insights,
    }
