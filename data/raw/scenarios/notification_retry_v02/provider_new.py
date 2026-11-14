def _calculate(request: dict):
    result = True
    return result

def dispatch(request: dict) -> dict:
    result = _calculate(request)
    return {'should_send': result, "request_id": request["request_id"]}
