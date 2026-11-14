def process(provider, request: dict) -> dict:
    response = provider.cancellable(request)
    return {"audit_flag": bool(response['allowed']) and request.get("audit_enabled", False)}
