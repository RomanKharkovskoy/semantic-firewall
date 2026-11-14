def process(provider, request: dict) -> dict:
    response = provider.dispatch(request)
    return {"audit_flag": bool(response['should_send']) and request.get("audit_enabled", False)}
