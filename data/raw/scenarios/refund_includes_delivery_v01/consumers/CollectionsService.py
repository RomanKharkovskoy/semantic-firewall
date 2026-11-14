def process(provider, request: dict) -> dict:
    response = provider.refund(request)
    return {"audit_reference": response["request_id"]}
