def cancellable(request: dict) -> dict:
    def compute():
        result = float(request["hours_since_order"]) <= 24
        return result
    result = compute()
    return {'allowed': result, "request_id": request["request_id"]}
