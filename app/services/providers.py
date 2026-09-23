from urllib.parse import quote_plus

PLATFORM_SEARCH = {
    "Amazon": "https://www.amazon.in/s?k={q}",
    "Flipkart": "https://www.flipkart.com/search?q={q}",
    "IKEA": "https://www.ikea.com/in/en/search/?q={q}",
    "Swiggy": "https://www.swiggy.com/search?query={q}",
    "Zomato": "https://www.zomato.com/search?q={q}",
    "OYO": "https://www.oyorooms.com/search?location={q}",
}

CATALOG = {
    "home": [
        ("Warm LED ceiling light", "Lighting", "IKEA", 1299),
        ("Minimal floor lamp", "Lighting", "Amazon", 1899),
        ("Compact study table", "Furniture", "Amazon", 4499),
        ("2-seater dining table", "Furniture", "IKEA", 7999),
        ("Decorative wall mirror", "Decor", "Flipkart", 1599),
        ("Neutral area rug", "Decor", "IKEA", 2999),
        ("Ceiling fan", "Utility", "Amazon", 2499),
        ("Storage cabinet", "Storage", "IKEA", 5999),
    ],
    "party": [
        ("Vegetarian catering package", "Catering", "Swiggy", 350),
        ("Party meal package", "Catering", "Zomato", 400),
        ("Birthday decoration kit", "Decoration", "Amazon", 1299),
        ("LED string-light decor", "Decoration", "Flipkart", 799),
        ("Budget hotel room", "Accommodation", "OYO", 1499),
        ("Disposable dinnerware set", "Supplies", "Amazon", 699),
    ],
    "jewelry": [
        ("Minimal gold-tone earrings", "Earrings", "Amazon", 799),
        ("Pearl drop earrings", "Earrings", "Flipkart", 999),
        ("Minimal pendant necklace", "Necklace", "Amazon", 1299),
        ("Statement oxidized necklace", "Necklace", "Flipkart", 1599),
        ("Slim bangle set", "Bangles", "Amazon", 699),
        ("Stone-studded bracelet", "Bracelet", "Flipkart", 899),
    ],
}

def search_url(platform: str, query: str) -> str:
    template = PLATFORM_SEARCH.get(platform, PLATFORM_SEARCH["Amazon"])
    return template.format(q=quote_plus(query))

def catalog_for(planner: str):
    return CATALOG[planner]
