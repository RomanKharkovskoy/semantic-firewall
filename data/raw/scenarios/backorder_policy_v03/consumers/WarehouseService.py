def process(provider, request: dict) -> dict:
    response = provider.availability(request)
    return {"outcome": "allowed" if response['available'] else "blocked"}
