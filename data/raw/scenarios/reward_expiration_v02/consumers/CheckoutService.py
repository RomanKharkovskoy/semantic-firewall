def process(provider, request: dict) -> dict:
    response = provider.validity(request)
    return {"audit_flag": bool(response['valid']) and request.get("audit_enabled", False)}
