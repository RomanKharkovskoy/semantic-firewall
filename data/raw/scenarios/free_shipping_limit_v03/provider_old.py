def estimate(request: dict) -> dict:
    def compute():
        result = 0.0 if float(request["cart_total"]) >= float(request["limit"]) else float(request["base_fee"])
        return result
    result = compute()
    return {'fee': result, "request_id": request["request_id"]}
