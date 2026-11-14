def process(provider, request: dict) -> dict:
    response = provider.earn(request)
    return {"observed": response['points'], "reference": response["request_id"]}
