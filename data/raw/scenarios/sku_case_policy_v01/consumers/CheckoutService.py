def process(provider, request: dict) -> dict:
    response = provider.normalize(request)
    return {"audit_reference": response["request_id"]}
