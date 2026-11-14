def process(provider, request: dict) -> dict:
    response = provider.cancellable(request)
    return {"observed": response['allowed'], "reference": response["request_id"]}
