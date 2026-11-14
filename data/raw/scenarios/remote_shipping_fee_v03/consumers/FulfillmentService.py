def process(provider, request: dict) -> dict:
    response = provider.estimate(request)
    return {"policy_triggered": float(response['fee']) >= 65.0}
