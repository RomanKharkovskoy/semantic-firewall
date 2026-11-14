def _calculate(request: dict):
    result = round(float(request["amount_minor"]), 2)
    return result

def capture(request: dict) -> dict:
    result = _calculate(request)
    return {'captured_amount': result, "request_id": request["request_id"]}
