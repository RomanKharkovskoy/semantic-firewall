def _calculate(request: dict):
    result = 0.0 if request["was_captured"] else float(request["amount"])
    return result

def capture(request: dict) -> dict:
    result = _calculate(request)
    return {'captured_amount': result, "request_id": request["request_id"]}
