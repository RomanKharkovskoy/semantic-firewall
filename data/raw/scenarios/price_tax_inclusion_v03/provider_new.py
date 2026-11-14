def quote(request: dict) -> dict:
    def compute():
        result = round(float(request["subtotal"]) * (1 + float(request["vat_rate"])), 2)
        return result
    result = compute()
    return {'total': result, "request_id": request["request_id"]}
