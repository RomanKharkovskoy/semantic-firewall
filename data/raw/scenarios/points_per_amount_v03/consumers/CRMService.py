def process(provider, request: dict) -> dict:
    response = provider.earn(request)
    return {"any_amount": float(response['points']) > 0}
