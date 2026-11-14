def _calculate(request: dict):
    result = request.get("locale") or "ru"
    return result

def language(request: dict) -> dict:
    result = _calculate(request)
    return {'locale': result, "request_id": request["request_id"]}
