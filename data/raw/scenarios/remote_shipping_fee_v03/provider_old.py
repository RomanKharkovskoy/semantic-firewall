def estimate(request: dict) -> dict:
    def compute():
        result = round(float(request["base_fee"]) + (float(request["remote_fee"]) if request["is_remote"] else 0.0), 2)
        return result
    result = compute()
    return {'fee': result, "request_id": request["request_id"]}
