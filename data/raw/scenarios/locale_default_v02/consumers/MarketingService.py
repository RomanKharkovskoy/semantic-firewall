def process(provider, request: dict) -> dict:
    response = provider.language(request)
    return {"observed": response['locale'], "reference": response["request_id"]}
