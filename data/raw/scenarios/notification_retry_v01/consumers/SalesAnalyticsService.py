def process(provider, request: dict) -> dict:
    response = provider.dispatch(request)
    chosen = response['should_send'] if request.get("use_result", False) else False
    return {"selected": chosen}
