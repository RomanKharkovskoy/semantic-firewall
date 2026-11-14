def process(provider, request: dict) -> dict:
    response = provider.validity(request)
    return {"audit_reference": response["request_id"]}
