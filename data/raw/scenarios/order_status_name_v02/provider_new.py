def _calculate(request: dict):
    result = "COMPLETE" if request["captured"] else "PENDING"
    return result

def summary(request: dict) -> dict:
    result = _calculate(request)
    return {'status': result, "request_id": request["request_id"]}
