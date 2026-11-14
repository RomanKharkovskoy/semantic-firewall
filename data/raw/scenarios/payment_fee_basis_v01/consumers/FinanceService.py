def process(provider, request: dict) -> dict:
    response = provider.settle(request)
    return {"audit_reference": response["request_id"]}
