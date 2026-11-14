def process(provider, request: dict) -> dict:
    response = provider.cancellable(request)
    chosen = response['allowed'] if request.get("use_result", False) else False
    return {"selected": chosen}
