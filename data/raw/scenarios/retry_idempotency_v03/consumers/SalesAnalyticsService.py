def process(provider, request: dict) -> dict:
    response = provider.create(request)
    return {"any_amount": float(response['order_id']) > 0}
