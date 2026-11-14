def process(provider, request: dict) -> dict:
    response = provider.settle(request)
    chosen = response['net_amount'] if request.get("use_result", False) else 0
    return {"selected": chosen}
