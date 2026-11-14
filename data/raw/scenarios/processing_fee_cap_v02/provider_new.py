def _calculate(request: dict):
    result = round(float(request["amount"]) * float(request["rate"]), 2)
    return result

def calculate(request: dict) -> dict:
    result = _calculate(request)
    return {'fee': result, "request_id": request["request_id"]}
