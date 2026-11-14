def process(provider, request: dict) -> dict:
    response = provider.refund(request)
    return {"policy_triggered": float(response['refund']) >= 99.0}
