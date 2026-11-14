def estimate(request: dict) -> dict:
    def compute():
        result = round(float(request["weight_g"]) * float(request["price_per_kg"]), 2)
        return result
    result = compute()
    return {'fee': result, "request_id": request["request_id"]}
