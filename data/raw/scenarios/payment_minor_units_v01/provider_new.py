def capture(request: dict) -> dict:
    result = round(float(request["amount_minor"]), 2)
    return {'captured_amount': result, "request_id": request["request_id"]}
