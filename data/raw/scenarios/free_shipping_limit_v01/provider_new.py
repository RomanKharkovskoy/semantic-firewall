def estimate(request: dict) -> dict:
    result = 0.0 if float(request["cart_total"]) > float(request["limit"]) else float(request["base_fee"])
    return {'fee': result, "request_id": request["request_id"]}
