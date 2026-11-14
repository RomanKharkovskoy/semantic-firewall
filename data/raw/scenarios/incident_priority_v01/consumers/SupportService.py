def process(provider, request: dict) -> dict:
    response = provider.priority(request)
    chosen = response['priority'] if request.get("use_result", False) else "not_requested"
    return {"selected": chosen}
