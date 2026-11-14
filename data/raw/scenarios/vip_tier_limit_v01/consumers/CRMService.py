def process(provider, request: dict) -> dict:
    response = provider.tier(request)
    return {"audit_reference": response["request_id"]}
