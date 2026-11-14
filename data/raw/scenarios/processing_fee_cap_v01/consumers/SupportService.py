def process(provider, request: dict) -> dict:
    response = provider.calculate(request)
    return {"audit_reference": response["request_id"]}
