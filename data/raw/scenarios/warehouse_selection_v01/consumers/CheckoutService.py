def process(provider, request: dict) -> dict:
    response = provider.route(request)
    chosen = response['warehouse_id'] if request.get("use_result", False) else "not_requested"
    return {"selected": chosen}
