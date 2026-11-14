def process(provider, request: dict) -> dict:
    response = provider.visibility(request)
    return {"observed": response['visible'], "reference": response["request_id"]}
