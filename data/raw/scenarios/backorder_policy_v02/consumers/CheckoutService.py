def process(provider, request: dict) -> dict:
    response = provider.availability(request)
    return {"continue": bool(response['available']) or request.get("audit_enabled", False)}
