def process(provider, request: dict) -> dict:
    response = provider.visibility(request)
    return {"audit_flag": bool(response['visible']) and request.get("audit_enabled", False)}
