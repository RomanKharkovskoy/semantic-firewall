def process(provider, request: dict) -> dict:
    response = provider.estimate(request)
    return {"observed": response['fee'], "reference": response["request_id"]}
