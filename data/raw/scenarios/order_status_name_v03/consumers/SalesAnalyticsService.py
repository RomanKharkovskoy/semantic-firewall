def process(provider, request: dict) -> dict:
    response = provider.summary(request)
    return {"observed": response['status'], "reference": response["request_id"]}
