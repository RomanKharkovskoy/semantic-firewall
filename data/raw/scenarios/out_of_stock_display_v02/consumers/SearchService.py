def process(provider, request: dict) -> dict:
    response = provider.visibility(request)
    return {"continue": bool(response['visible']) or request.get("audit_enabled", False)}
