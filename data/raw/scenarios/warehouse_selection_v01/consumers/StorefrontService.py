def process(provider, request: dict) -> dict:
    response = provider.route(request)
    return {"audit_reference": response["request_id"]}
