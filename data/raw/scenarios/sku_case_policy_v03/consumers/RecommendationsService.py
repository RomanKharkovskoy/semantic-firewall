def process(provider, request: dict) -> dict:
    response = provider.normalize(request)
    return {"observed": response['sku'], "reference": response["request_id"]}
