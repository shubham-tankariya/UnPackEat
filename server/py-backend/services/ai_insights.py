"""
ai_insights.py -- Generate contextual AI commentary using OpenAI.

Uses gpt-4o-mini (cheap, fast, extremely reliable JSON).
Runs only if OPENAI_API_KEY is set; otherwise returns None.
"""

import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = None


def _get_client():
    """Lazy initialize OpenAI client."""
    global client
    if client is not None:
        return client, None

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None, "OPENAI_API_KEY not set in .env"

    try:
        client = OpenAI(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"OpenAI initialization failed: {e}"


INSIGHT_PROMPT = """You are a nutritionist AI. Given this product data, provide a concise health analysis.

Product: {name} by {brand}
Health Score: {score}/100 ({verdict})
Nutrients per 100g: {nutrients}
Ingredients: {ingredients_text}
Additives: {additives}
Concerns: {concerns}
Likes: {likes}
NOVA Group: {nova}

Respond with ONLY valid JSON (no markdown, no code fences):
{{
  "summary": "One compelling sentence summarizing this product's health profile",
  "detailed_analysis": "2-3 sentences explaining the key health implications of consuming this product regularly",
  "better_alternatives": "Suggest 2-3 healthier alternatives in the same product category, be specific",
  "who_should_avoid": "List specific groups who should limit or avoid this product and why",
  "ideal_consumption": "Practical guidance on how often and how much is reasonable"
}}
"""


def _escape(text):
    """Escapes {} to prevent str.format() errors."""
    if not isinstance(text, str):
        return text
    return text.replace("{", "{{").replace("}", "}}")


def _retry_request(call, retries=2):
    for attempt in range(retries + 1):
        try:
            return call()
        except Exception as e:
            err = str(e).lower()
            if ("rate" in err or "quota" in err) and attempt < retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise


def generate_insights(normalized, analyzed):
    """
    Generate AI-powered insights for the product.
    Returns dict with insights, or dict with status/reason on failure.
    """
    client, reason = _get_client()
    if client is None:
        return {"status": "unavailable", "reason": reason}

    product = normalized.get("product", {})
    highlights = analyzed.get("highlights", {})
    nutrients = json.dumps(normalized.get("nutrients", {}), default=str)

    prompt = INSIGHT_PROMPT.format(
        name=_escape(product.get("name", "Unknown")),
        brand=_escape(product.get("brand", "Unknown")),
        score=highlights.get("health_score", "?"),
        verdict=_escape(highlights.get("verdict", "?")),
        nutrients=_escape(nutrients),
        ingredients_text=_escape(product.get("ingredients_text", "")[:500]),
        additives=", ".join(a.get("code", "") for a in analyzed.get("additives_full", [])) or "None",
        concerns=", ".join(highlights.get("concerns", [])) or "None",
        likes=", ".join(highlights.get("likes", [])) or "None",
        nova=highlights.get("nova_group", "?"),
    )

    try:
        resp = _retry_request(lambda: client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        ))

        text = resp.choices[0].message.content
        return json.loads(text)

    except Exception as e:
        return {"status": "error", "reason": str(e)}