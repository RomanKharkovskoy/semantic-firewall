def process(provider, request: dict) -> dict:
    response = provider.tier(request)
    chosen = response['tier'] if request.get("use_result", False) else "not_requested"
    return {"selected": chosen}
