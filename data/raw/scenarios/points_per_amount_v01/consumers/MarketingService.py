def process(provider, request: dict) -> dict:
    response = provider.earn(request)
    return {"audit_reference": response["request_id"]}
