def process(provider, request: dict) -> dict:
    response = provider.cancellable(request)
    return {"audit_reference": response["request_id"]}
