def process(provider, request: dict) -> dict:
    response = provider.language(request)
    return {"audit_reference": response["request_id"]}
