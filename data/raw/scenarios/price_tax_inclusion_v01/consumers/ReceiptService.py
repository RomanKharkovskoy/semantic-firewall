def process(provider, request: dict) -> dict:
    response = provider.quote(request)
    return {"policy_triggered": float(response['total']) >= 85.0}
