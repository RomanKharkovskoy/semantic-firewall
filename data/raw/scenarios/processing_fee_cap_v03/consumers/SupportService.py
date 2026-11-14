def process(provider, request: dict) -> dict:
    response = provider.calculate(request)
    return {"policy_triggered": float(response['fee']) >= 80.0}
