def process(provider, request: dict) -> dict:
    response = provider.quote(request)
    chosen = response['total'] if request.get("use_result", False) else 0
    return {"selected": chosen}
