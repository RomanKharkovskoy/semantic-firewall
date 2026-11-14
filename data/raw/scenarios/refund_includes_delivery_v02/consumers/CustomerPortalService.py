def process(provider, request: dict) -> dict:
    response = provider.refund(request)
    return {"any_amount": float(response['refund']) > 0}
