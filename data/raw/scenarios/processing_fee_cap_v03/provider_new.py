def calculate(request: dict) -> dict:
    def compute():
        result = round(float(request["amount"]) * float(request["rate"]), 2)
        return result
    result = compute()
    return {'fee': result, "request_id": request["request_id"]}
