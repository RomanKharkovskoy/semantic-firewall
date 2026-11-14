def process(provider, request: dict) -> dict:
    response = provider.earn(request)
    chosen = response['points'] if request.get("use_result", False) else 0
    return {"selected": chosen}
