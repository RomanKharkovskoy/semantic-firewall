def process(provider, request: dict) -> dict:
    response = provider.create(request)
    chosen = response['order_id'] if request.get("use_result", False) else 0
    return {"selected": chosen}
