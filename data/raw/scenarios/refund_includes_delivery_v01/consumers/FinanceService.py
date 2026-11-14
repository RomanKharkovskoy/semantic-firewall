def process(provider, request: dict) -> dict:
    response = provider.refund(request)
    return {"observed": response['refund'], "reference": response["request_id"]}
