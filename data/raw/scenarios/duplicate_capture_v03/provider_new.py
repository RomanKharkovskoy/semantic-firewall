def capture(request: dict) -> dict:
    def compute():
        result = float(request["amount"])
        return result
    result = compute()
    return {'captured_amount': result, "request_id": request["request_id"]}
