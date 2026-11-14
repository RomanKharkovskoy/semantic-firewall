def _calculate(request: dict):
    result = round(float(request["subtotal"]) * (1 + float(request["vat_rate"])) - float(request["coupon"]), 2)
    return result

def quote(request: dict) -> dict:
    result = _calculate(request)
    return {'total': result, "request_id": request["request_id"]}
