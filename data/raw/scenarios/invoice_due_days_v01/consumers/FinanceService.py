def process(provider, request: dict) -> dict:
    response = provider.deadline(request)
    return {"audit_reference": response["request_id"]}
