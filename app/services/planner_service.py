from app.services.ai_service import generate_ai, normalize_ai
from app.services.providers import catalog_for, search_url

def _fallback(planner, budget, context):
    rows = catalog_for(planner)
    recommendations = []
    for name, category, platform, price in rows:
        if price <= max(budget * 0.35, 1):
            recommendations.append({
                "name": name,
                "category": category,
                "platform": platform,
                "estimated_price": price,
                "reason": f"Selected as a practical {category.lower()} option within the stated budget.",
                "search_url": search_url(platform, name),
                "budget_fit": "Within budget",
            })
    if not recommendations:
        recommendations = [{
            "name": rows[0][0], "category": rows[0][1], "platform": rows[0][2],
            "estimated_price": rows[0][3], "reason": "Starter option from the demo provider catalog.",
            "search_url": search_url(rows[0][2], rows[0][0]), "budget_fit": "Check price",
        }]
    recommendations = recommendations[:8]

    if planner == "home":
        allocation = {"furniture": round(budget*.40), "lighting": round(budget*.15), "decor": round(budget*.20), "storage": round(budget*.25)}
        summary = f"Home plan for {context['rooms']} with a {context['style']} style."
        tips = ["Prioritize essential furniture before decorative pieces.", "Measure rooms before buying large items.", "Keep a 5–10% buffer for delivery or installation."]
    elif planner == "party":
        allocation = {"food": round(budget*.45), "decoration": round(budget*.15), "venue": round(budget*.25), "entertainment": round(budget*.15)}
        summary = f"{context['event_type']} plan for {context['guests']} guests at {context['venue']}."
        tips = ["Confirm per-person food pricing before booking.", "Reserve a small contingency for last-minute needs.", "Compare venue and catering package totals, not only headline prices."]
    else:
        allocation = {"jewelry": round(budget*.80), "buffer": round(budget*.20)}
        summary = f"Jewelry plan for a {context['occasion']} occasion in a {context['style']} style."
        tips = ["Match jewelry to the outfit neckline and dominant color.", "Use one statement piece and keep supporting pieces simpler.", "Check material, size and return policy before purchasing."]
    return {
        "planner": planner, "budget": budget, "budget_summary": summary,
        "allocation": allocation, "recommendations": recommendations,
        "tips": tips,
        "disclaimer": "Demo prices are estimates. Provider links are search links, not live product inventory.",
    }

def generate_home(budget, rooms, style, needs):
    fallback = _fallback("home", budget, {"rooms": rooms, "style": style, "needs": needs})
    prompt = f"""You are PocketSmart AI, a budget-aware home interior recommendation assistant.
User budget: INR {budget}
Rooms: {rooms}
Style: {style}
Needs: {needs}
Create practical recommendations. Do not claim live prices or availability. Use the supplied provider names only as shopping destinations.
Return JSON matching the requested schema with 5-8 recommendations, sensible INR estimates, category allocation summing approximately to the budget, and concise tips."""
    try:
        return normalize_ai(generate_ai(prompt), "home", budget)
    except Exception:
        return fallback

def generate_party(budget, guests, event_type, venue, preferences):
    fallback = _fallback("party", budget, {"guests": guests, "event_type": event_type, "venue": venue, "preferences": preferences})
    prompt = f"""You are PocketSmart AI, a budget-aware party planner.
Budget: INR {budget}
Guests: {guests}
Event type: {event_type}
Venue details: {venue}
Preferences: {preferences}
Allocate the budget across food, venue, decoration and entertainment. Give 5-8 practical suggestions. Do not claim live vendor availability or live prices. Return structured JSON."""
    try:
        return normalize_ai(generate_ai(prompt), "party", budget)
    except Exception:
        return fallback

def generate_jewelry(budget, occasion, style, outfit_description, image_bytes=None, image_type=None):
    fallback = _fallback("jewelry", budget, {"occasion": occasion, "style": style, "outfit_description": outfit_description})
    prompt = f"""You are PocketSmart AI, a jewelry styling assistant.
Budget: INR {budget}
Occasion: {occasion}
Preferred style: {style}
Outfit description: {outfit_description}
If an outfit image is attached, use it only to infer broad colors, neckline, and aesthetic. Do not identify the person.
Recommend 5-8 jewelry options from the allowed shopping platforms. Do not claim live prices or inventory. Return structured JSON."""
    try:
        return normalize_ai(generate_ai(prompt, image_bytes, image_type), "jewelry", budget)
    except Exception:
        return fallback
