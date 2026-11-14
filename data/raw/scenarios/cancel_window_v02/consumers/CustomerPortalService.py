def process(provider, request: dict) -> dict:
    response = provider.cancellable(request)
    return {"outcome": "allowed" if response['allowed'] else "blocked"}
