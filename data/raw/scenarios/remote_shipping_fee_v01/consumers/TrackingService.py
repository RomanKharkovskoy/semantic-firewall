def process(provider, request: dict) -> dict:
    response = provider.estimate(request)
    return {"audit_reference": response["request_id"]}
