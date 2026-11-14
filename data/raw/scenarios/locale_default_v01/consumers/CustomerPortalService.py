def process(provider, request: dict) -> dict:
    response = provider.language(request)
    chosen = response['locale'] if request.get("use_result", False) else "not_requested"
    return {"selected": chosen}
