def process(provider, request: dict) -> dict:
    response = provider.dispatch(request)
    return {"outcome": "allowed" if response['should_send'] else "blocked"}
