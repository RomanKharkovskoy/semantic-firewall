def calculate(request: dict) -> dict:
    result = round(float(request["amount"]) * float(request["rate"]), 2)
    return {'fee': result, "request_id": request["request_id"]}
