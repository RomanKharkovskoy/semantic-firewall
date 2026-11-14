def process(provider, request: dict) -> dict:
    response = provider.dispatch(request)
    return {"audit_reference": response["request_id"]}
