def process(provider, request: dict) -> dict:
    response = provider.top_item(request)
    chosen = response['sku'] if request.get("use_result", False) else "not_requested"
    return {"selected": chosen}
