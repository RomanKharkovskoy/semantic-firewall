def process(provider, request: dict) -> dict:
    response = provider.calculate(request)
    return {"any_amount": float(response['fee']) > 0}
