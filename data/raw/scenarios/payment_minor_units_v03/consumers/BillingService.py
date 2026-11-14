def process(provider, request: dict) -> dict:
    response = provider.capture(request)
    return {"any_amount": float(response['captured_amount']) > 0}
