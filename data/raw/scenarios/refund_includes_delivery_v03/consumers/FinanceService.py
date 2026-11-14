def process(provider, request: dict) -> dict:
    response = provider.refund(request)
    return {"policy_triggered": float(response['refund']) >= 170.0}
