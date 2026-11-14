def estimate(request: dict) -> dict:
    def compute():
        result = round(float(request["base_fee"]), 2)
        return result
    result = compute()
    return {'fee': result, "request_id": request["request_id"]}
