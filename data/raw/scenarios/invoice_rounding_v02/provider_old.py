from decimal import Decimal, ROUND_HALF_EVEN

def _calculate(request: dict):
    result = float(Decimal(str(request["amount"])).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN))
    return result

def quote(request: dict) -> dict:
    result = _calculate(request)
    return {'total': result, "request_id": request["request_id"]}
