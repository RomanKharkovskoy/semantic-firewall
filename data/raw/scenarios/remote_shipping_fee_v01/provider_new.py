def estimate(request: dict) -> dict:
    result = round(float(request["base_fee"]), 2)
    return {'fee': result, "request_id": request["request_id"]}
