def process(provider, request: dict) -> dict:
    response = provider.top_item(request)
    return {"observed": response['sku'], "reference": response["request_id"]}
