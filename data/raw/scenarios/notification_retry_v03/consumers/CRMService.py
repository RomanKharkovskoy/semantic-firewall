def process(provider, request: dict) -> dict:
    response = provider.dispatch(request)
    return {"continue": bool(response['should_send']) or request.get("audit_enabled", False)}
