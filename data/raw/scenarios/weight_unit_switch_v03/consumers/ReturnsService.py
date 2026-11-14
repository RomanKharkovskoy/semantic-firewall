def process(provider, request: dict) -> dict:
    response = provider.estimate(request)
    chosen = response['fee'] if request.get("use_result", False) else 0
    return {"selected": chosen}
