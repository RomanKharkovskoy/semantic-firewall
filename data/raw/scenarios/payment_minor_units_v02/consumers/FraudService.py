def process(provider, request: dict) -> dict:
    response = provider.capture(request)
    return {"observed": response['captured_amount'], "reference": response["request_id"]}
