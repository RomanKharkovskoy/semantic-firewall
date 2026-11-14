def _calculate(request: dict):
    result = "urgent" if request["severity"] == "high" else "normal"
    return result

def priority(request: dict) -> dict:
    result = _calculate(request)
    return {'priority': result, "request_id": request["request_id"]}
