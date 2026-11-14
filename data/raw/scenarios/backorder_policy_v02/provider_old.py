def _calculate(request: dict):
    result = int(request["on_hand"]) >= int(request["requested"])
    return result

def availability(request: dict) -> dict:
    result = _calculate(request)
    return {'available': result, "request_id": request["request_id"]}
