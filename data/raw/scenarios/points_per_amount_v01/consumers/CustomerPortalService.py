def process(provider, request: dict) -> dict:
    response = provider.earn(request)
    return {"policy_triggered": float(response['points']) >= 10.0}
