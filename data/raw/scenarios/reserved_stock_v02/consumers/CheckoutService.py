def process(provider, request: dict) -> dict:
    response = provider.availability(request)
    chosen = response['available'] if request.get("use_result", False) else 0
    return {"selected": chosen}
