def process(provider, request: dict) -> dict:
    response = provider.create(request)
    return {"observed": response['order_id'], "reference": response["request_id"]}
