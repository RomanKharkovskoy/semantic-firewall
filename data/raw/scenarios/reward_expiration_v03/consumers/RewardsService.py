def process(provider, request: dict) -> dict:
    response = provider.validity(request)
    return {"continue": bool(response['valid']) or request.get("audit_enabled", False)}
