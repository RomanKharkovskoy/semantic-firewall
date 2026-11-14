def process(provider, request: dict) -> dict:
    response = provider.availability(request)
    return {"audit_flag": bool(response['available']) and request.get("audit_enabled", False)}
