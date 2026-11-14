def process(provider, request: dict) -> dict:
    response = provider.tier(request)
    return {"observed": response['tier'], "reference": response["request_id"]}
