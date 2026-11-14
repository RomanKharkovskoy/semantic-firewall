def process(provider, request: dict) -> dict:
    response = provider.validity(request)
    return {"observed": response['valid'], "reference": response["request_id"]}
