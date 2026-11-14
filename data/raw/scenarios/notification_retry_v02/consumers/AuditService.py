def process(provider, request: dict) -> dict:
    response = provider.dispatch(request)
    return {"observed": response['should_send'], "reference": response["request_id"]}
