def process(provider, request: dict) -> dict:
    response = provider.validity(request)
    chosen = response['valid'] if request.get("use_result", False) else False
    return {"selected": chosen}
