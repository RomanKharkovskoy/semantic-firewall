def _calculate(request: dict):
    result = round(float(request["item_amount"]), 2)
    return result

def refund(request: dict) -> dict:
    result = _calculate(request)
    return {'refund': result, "request_id": request["request_id"]}
