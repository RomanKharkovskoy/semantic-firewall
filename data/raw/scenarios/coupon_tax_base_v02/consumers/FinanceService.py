def process(provider, request: dict) -> dict:
    response = provider.quote(request)
    return {"observed": response['total'], "reference": response["request_id"]}
