def process(provider, request: dict) -> dict:
    response = provider.visibility(request)
    return {"outcome": "allowed" if response['visible'] else "blocked"}
