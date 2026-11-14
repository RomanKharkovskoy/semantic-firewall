def process(provider, request: dict) -> dict:
    response = provider.availability(request)
    return {"any_amount": float(response['available']) > 0}
