def process(provider, request: dict) -> dict:
    response = provider.capture(request)
    chosen = response['captured_amount'] if request.get("use_result", False) else 0
    return {"selected": chosen}
