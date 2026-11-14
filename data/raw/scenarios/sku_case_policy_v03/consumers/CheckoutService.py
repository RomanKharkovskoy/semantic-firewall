def process(provider, request: dict) -> dict:
    response = provider.normalize(request)
    chosen = response['sku'] if request.get("use_result", False) else "not_requested"
    return {"selected": chosen}
