def process(provider, request: dict) -> dict:
    response = provider.validity(request)
    return {"outcome": "allowed" if response['valid'] else "blocked"}
