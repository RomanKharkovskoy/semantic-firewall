def process(provider, request: dict) -> dict:
    response = provider.refund(request)
    chosen = response['refund'] if request.get("use_result", False) else 0
    return {"selected": chosen}
