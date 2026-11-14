def _calculate(request: dict):
    result = int(float(request["spent"]) // 10)
    return result

def earn(request: dict) -> dict:
    result = _calculate(request)
    return {'points': result, "request_id": request["request_id"]}
