def calculate(request: dict) -> dict:
    result = round(min(float(request["amount"]) * float(request["rate"]), float(request["cap"])), 2)
    return {'fee': result, "request_id": request["request_id"]}
