def process(provider, request: dict) -> dict:
    response = provider.quote(request)
    return {"any_amount": float(response['total']) > 0}
