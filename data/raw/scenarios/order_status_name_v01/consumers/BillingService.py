def process(provider, request: dict) -> dict:
    response = provider.summary(request)
    chosen = response['status'] if request.get("use_result", False) else "not_requested"
    return {"selected": chosen}
