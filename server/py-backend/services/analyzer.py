# analyzer.py

import json
import os

# Load additive info from the shared knowledge base
_ADDITIVES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "additives.json")
with open(_ADDITIVES_PATH, encoding="utf-8") as _f:
    ADDITIVE_INFO: dict = json.load(_f)

# Additive risk → score deduction
ADDITIVE_PENALTY = {"high": 10, "moderate": 4, "low": 0, "unknown": 2}


def rating_color(metric, value):
    """Traffic-light colour for individual nutrients."""
    if value is None:
        return "neutral"
    if metric == "salt":
        return "red" if value > 1.5 else "orange" if value > 0.6 else "green"
    if metric == "saturated_fat":
        return "red" if value > 5 else "orange" if value > 2.5 else "green"
    if metric == "sugars":
        return "red" if value > 15 else "orange" if value > 8 else "green"
    if metric == "fat":
        return "red" if value > 17.5 else "orange" if value > 10 else "green"
    if metric == "fiber":
        return "green" if value >= 3 else "orange" if value > 1 else "red"
    if metric == "protein":
        return "green" if value >= 10 else "neutral"
    if metric == "energy_kcal":
        return "red" if value > 400 else "orange" if value > 250 else "green"
    return "neutral"


def _safe(val):
    """Return val as float if it's a valid number, else None."""
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _key_nutrients_present(n):
    """Count how many of the four key nutrients are actually reported."""
    return sum(
        1 for k in ("salt", "saturated_fat", "sugars", "fiber")
        if _safe(n.get(k)) is not None
    )

# Labels that deserve a positive signal
_POSITIVE_LABELS = {
    "en:organic", "en:eu-organic", "en:fair-trade",
    "en:rainforest-alliance", "en:vegan", "en:vegetarian",
    "en:no-artificial-flavours", "en:no-artificial-colours",
    "en:no-preservatives", "en:whole-grain",
}


def analyze(normalized):
    n   = normalized["nutrients"]
    ing = normalized["ingredients"]
    m   = normalized["metadata"]
    s   = normalized["serving"]

    # ------------------------------------------------------------------ #
    #  NUTRITION DATA PER WARNING                                         #
    #  If OFF says values are per-serving (not per 100g), our analysis   #
    #  will be inaccurate — flag it prominently.                          #
    # ------------------------------------------------------------------ #
    nutrition_data_per = s.get("nutrition_data_per", "100g")


    score    = 100
    likes    = []
    concerns = []

    salt        = _safe(n.get("salt"))
    sat_fat     = _safe(n.get("saturated_fat"))
    total_fat   = _safe(n.get("fat"))
    sugars      = _safe(n.get("sugars"))
    fiber       = _safe(n.get("fiber"))
    protein     = _safe(n.get("protein"))
    energy_kcal = _safe(n.get("energy_kcal"))

    # ------------------------------------------------------------------ #
    #  SALT                                                               #
    # ------------------------------------------------------------------ #
    # Guard against erroneous OFF data (salt > 100 g/100 g is impossible)
    if salt is not None and salt > 100:
        salt = None

    if salt is None:
        score -= 5
        concerns.append("Salt content not reported")
    elif salt > 1.5:
        score -= 25
        concerns.append("Very high salt")
    elif salt > 0.6:
        score -= 12
        concerns.append("Moderate salt")
    else:
        likes.append("Low salt")

    # ------------------------------------------------------------------ #
    #  SATURATED FAT                                                      #
    # ------------------------------------------------------------------ #
    if sat_fat is None:
        score -= 5
        concerns.append("Saturated fat not reported")
    elif sat_fat > 5:
        score -= 20
        concerns.append("High saturated fat")
    elif sat_fat > 2.5:
        score -= 8
        concerns.append("Moderate saturated fat")
    else:
        likes.append("Low saturated fat")

    # ------------------------------------------------------------------ #
    #  TOTAL FAT                                                          #
    # ------------------------------------------------------------------ #
    if total_fat is not None:
        if total_fat > 17.5:
            score -= 10
            concerns.append("High total fat")
        elif total_fat > 10:
            score -= 4

    # ------------------------------------------------------------------ #
    #  SUGARS                                                             #
    # ------------------------------------------------------------------ #
    if sugars is None:
        score -= 3
        concerns.append("Sugar content not reported")
    elif sugars > 22.5:
        score -= 20
        concerns.append("Very high sugar")
    elif sugars > 12.5:
        score -= 10
        concerns.append("High sugar")
    elif sugars > 8:
        score -= 4
        concerns.append("Moderate sugar")
    else:
        likes.append("Low sugar")

    # ------------------------------------------------------------------ #
    #  FIBER                                                              #
    # ------------------------------------------------------------------ #
    if fiber is not None:
        if fiber >= 5:
            score += 8
            likes.append("Excellent fiber content")
        elif fiber >= 3:
            score += 4
            likes.append("Good fiber content")
        elif fiber < 1:
            score -= 3

    # ------------------------------------------------------------------ #
    #  PROTEIN                                                            #
    # ------------------------------------------------------------------ #
    if protein is not None and protein >= 10:
        score += 5
        likes.append("High protein")

    # ------------------------------------------------------------------ #
    #  ENERGY DENSITY                                                     #
    # ------------------------------------------------------------------ #
    if energy_kcal is not None:
        if energy_kcal > 450:
            score -= 10
            concerns.append("Very high calorie density")
        elif energy_kcal > 300:
            score -= 5
            concerns.append("High calorie density")

    # ------------------------------------------------------------------ #
    #  NOVA GROUP (processing level)                                      #
    # ------------------------------------------------------------------ #
    nova = m.get("nova_group")
    if nova == 4:
        score -= 15
        concerns.append("Ultra-processed food (NOVA 4)")
    elif nova == 3:
        score -= 5
        concerns.append("Processed food (NOVA 3)")
    elif nova in (1, 2):
        likes.append("Minimally processed")

    # ------------------------------------------------------------------ #
    #  PALM OIL                                                           #
    # ------------------------------------------------------------------ #
    if ing.get("contains_palm_oil"):
        score -= 5
        concerns.append("Contains palm oil")

    # ------------------------------------------------------------------ #
    #  ADDITIVES  (loaded from data/additives.json)                      #
    # ------------------------------------------------------------------ #
    additives_full = []
    additive_score_deduction = 0
    high_risk_count = 0

    for a in ing.get("additives", []):
        code = (a.get("id") or "").replace("en:", "").upper()
        info = ADDITIVE_INFO.get(code, {
            "name": a.get("text") or code,
            "category": "Unknown",
            "risk": "unknown",
            "explanation": "No safety data available.",
        })
        additives_full.append({
            "code":        code,
            "name":        info.get("name", code),
            "category":    info.get("category", "Unknown"),
            "risk":        info.get("risk", "unknown"),
            "explanation": info.get("explanation", "No safety data available."),
        })
        deduction = ADDITIVE_PENALTY.get(info.get("risk", "unknown"), 2)
        additive_score_deduction += deduction
        if info.get("risk") == "high":
            high_risk_count += 1

    # Cap additive penalty at 20 points
    additive_score_deduction = min(additive_score_deduction, 20)
    if additive_score_deduction > 0:
        score -= additive_score_deduction
    if high_risk_count:
        concerns.append(f"{high_risk_count} high-risk additive(s) detected")

    # ------------------------------------------------------------------ #
    #  POSITIVE LABEL BONUSES                                            #
    # ------------------------------------------------------------------ #
    product_labels = set(m.get("labels") or [])
    matched_labels = product_labels & _POSITIVE_LABELS
    if matched_labels:
        score += min(5, len(matched_labels) * 2)
        label_names = [l.replace("en:", "").replace("-", " ").title() for l in sorted(matched_labels)]
        likes.append(f"Certified: {', '.join(label_names)}")

    # ------------------------------------------------------------------ #
    #  DATA COMPLETENESS                                                  #
    #  Prefer OFF's own completeness score; fall back to key-nutrient    #
    #  count if not available.                                            #
    # ------------------------------------------------------------------ #
    off_completeness = _safe(m.get("off_completeness"))
    if nutrition_data_per != "100g":
        score -= 8
        concerns.append(f"Nutrition values reported per-serving, not per-100g — analysis may be inaccurate")
    elif off_completeness is not None:
        if off_completeness >= 0.8:
            score += 3
        elif off_completeness < 0.35:
            score -= 5
            concerns.append("Very limited nutrition data available")
    else:
        key_present = _key_nutrients_present(n)
        if key_present == 4:
            score += 3
        elif key_present <= 1:
            score -= 5
            concerns.append("Very limited nutrition data available")

    # ------------------------------------------------------------------ #
    #  CLAMP                                                              #
    # ------------------------------------------------------------------ #
    score = max(0, min(100, score))

    # ------------------------------------------------------------------ #
    #  RDA TABLE                                                          #
    # ------------------------------------------------------------------ #
    RDA = {
        "salt":          5,
        "saturated_fat": 20,
        "sugars":        50,
        "fiber":         25,
        "protein":       50,
        "fat":           70,
        "energy_kcal":   2000,
        "carbohydrates": 260,
        "cholesterol":   0.3,   # 300 mg/day = 0.3 g
    }

    nutrients_list = []
    for key, val in n.items():
        v = _safe(val)
        if v is not None:
            nutrients_list.append({
                "name":        key,
                "amount_100g": v,
                "unit":        "kcal" if key == "energy_kcal" else "g",
                "rda_percent": round((v / RDA.get(key, 100)) * 100, 1),
                "rating":      rating_color(key, v),
            })

    # ------------------------------------------------------------------ #
    #  PER-SERVING NUTRIENTS                                              #
    # ------------------------------------------------------------------ #
    sg = s.get("serving_size_g")
    if sg:
        per_serv = {
            k: round((_safe(v) * sg) / 100, 2)
            for k, v in n.items()
            if _safe(v) is not None
        }
    else:
        per_serv = None

    # ------------------------------------------------------------------ #
    #  RADAR (0–1 scale)                                                  #
    # ------------------------------------------------------------------ #
    radar = {
        "salt":          min(1.0, (_safe(n.get("salt"))          or 0) / 3),
        "saturated_fat": min(1.0, (_safe(n.get("saturated_fat")) or 0) / 10),
        "sugars":        min(1.0, (_safe(n.get("sugars"))        or 0) / 25),
        "energy":        min(1.0, (_safe(n.get("energy_kcal"))   or 0) / 600),
        "fiber":         min(1.0, (_safe(n.get("fiber"))         or 0) / 10),
        "protein":       min(1.0, (_safe(n.get("protein"))       or 0) / 25),
    }

    # ------------------------------------------------------------------ #
    #  VERDICT                                                            #
    # ------------------------------------------------------------------ #
    if score >= 75:
        verdict = "Healthy choice"
    elif score >= 50:
        verdict = "Moderate consumption recommended"
    elif score >= 25:
        verdict = "Best enjoyed occasionally"
    else:
        verdict = "Limit consumption"

    return {
        "highlights": {
            "health_score": score,
            "verdict":      verdict,
            "likes":        likes,
            "concerns":     concerns,
            "nova_group":   nova,
        },
        "nutrients":      nutrients_list,
        "nutrient_radar": radar,
        "additives_full": additives_full,
        "serving": {
            "per_100g":       n,
            "per_serving":    per_serv,
            "serving_size_g": sg,
        },
    }
