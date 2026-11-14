def _calculate(request: dict):
    result = max(0, int(request["on_hand"]) - int(request["reserved"]))
    return result

def availability(request: dict) -> dict:
    result = _calculate(request)
    return {'available': result, "request_id": request["request_id"]}
