def process(provider, request: dict) -> dict:
    response = provider.cancellable(request)
    return {"continue": bool(response['allowed']) or request.get("audit_enabled", False)}
