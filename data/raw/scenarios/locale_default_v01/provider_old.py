def language(request: dict) -> dict:
    result = request.get("locale") or "ru"
    return {'locale': result, "request_id": request["request_id"]}
