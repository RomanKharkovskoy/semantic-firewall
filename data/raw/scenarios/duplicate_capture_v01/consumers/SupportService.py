def process(provider, request: dict) -> dict:
    response = provider.capture(request)
    return {"policy_triggered": float(response['captured_amount']) >= 0.0}
