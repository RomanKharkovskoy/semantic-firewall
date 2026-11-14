def process(provider, request: dict) -> dict:
    response = provider.create(request)
    return {"audit_reference": response["request_id"]}
