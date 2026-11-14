def process(provider, request: dict) -> dict:
    response = provider.settle(request)
    return {"policy_triggered": float(response['net_amount']) >= 127.5}
