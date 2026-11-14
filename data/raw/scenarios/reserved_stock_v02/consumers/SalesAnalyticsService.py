def process(provider, request: dict) -> dict:
    response = provider.availability(request)
    return {"observed": response['available'], "reference": response["request_id"]}
