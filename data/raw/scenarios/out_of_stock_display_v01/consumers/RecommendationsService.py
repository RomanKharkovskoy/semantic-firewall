def process(provider, request: dict) -> dict:
    response = provider.visibility(request)
    chosen = response['visible'] if request.get("use_result", False) else False
    return {"selected": chosen}
