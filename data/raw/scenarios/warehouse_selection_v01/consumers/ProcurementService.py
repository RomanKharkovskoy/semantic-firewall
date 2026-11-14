def process(provider, request: dict) -> dict:
    response = provider.route(request)
    return {"observed": response['warehouse_id'], "reference": response["request_id"]}
