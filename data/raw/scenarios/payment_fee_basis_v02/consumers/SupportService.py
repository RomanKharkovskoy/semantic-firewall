def process(provider, request: dict) -> dict:
    response = provider.settle(request)
    return {"any_amount": float(response['net_amount']) > 0}
