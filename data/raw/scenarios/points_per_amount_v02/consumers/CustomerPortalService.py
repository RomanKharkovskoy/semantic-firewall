def process(provider, request: dict) -> dict:
    response = provider.earn(request)
    return {"policy_triggered": float(response['points']) >= 5.0}
