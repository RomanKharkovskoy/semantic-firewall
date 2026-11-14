def calculate(request: dict) -> dict:
    def compute():
        result = round(min(float(request["amount"]) * float(request["rate"]), float(request["cap"])), 2)
        return result
    result = compute()
    return {'fee': result, "request_id": request["request_id"]}
