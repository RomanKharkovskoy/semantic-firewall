from decimal import Decimal, ROUND_HALF_EVEN

def quote(request: dict) -> dict:
    def compute():
        result = float(Decimal(str(request["amount"])).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN))
        return result
    result = compute()
    return {'total': result, "request_id": request["request_id"]}
