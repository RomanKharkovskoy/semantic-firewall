def process(provider, request: dict) -> dict:
    response = provider.priority(request)
    return {"observed": response['priority'], "reference": response["request_id"]}
