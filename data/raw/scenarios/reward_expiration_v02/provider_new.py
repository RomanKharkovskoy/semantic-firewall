def _calculate(request: dict):
    result = int(request["days_old"]) <= 14
    return result

def validity(request: dict) -> dict:
    result = _calculate(request)
    return {'valid': result, "request_id": request["request_id"]}
