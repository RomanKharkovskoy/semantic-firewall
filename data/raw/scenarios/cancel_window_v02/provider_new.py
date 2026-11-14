def _calculate(request: dict):
    result = float(request["hours_since_order"]) < 24
    return result

def cancellable(request: dict) -> dict:
    result = _calculate(request)
    return {'allowed': result, "request_id": request["request_id"]}
