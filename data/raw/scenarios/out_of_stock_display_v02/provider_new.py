def _calculate(request: dict):
    result = int(request["stock"]) > 0 or bool(request["allow_backorder"])
    return result

def visibility(request: dict) -> dict:
    result = _calculate(request)
    return {'visible': result, "request_id": request["request_id"]}
