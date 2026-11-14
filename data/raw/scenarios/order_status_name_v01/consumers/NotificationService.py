def process(provider, request: dict) -> dict:
    response = provider.summary(request)
    return {"audit_reference": response["request_id"]}
