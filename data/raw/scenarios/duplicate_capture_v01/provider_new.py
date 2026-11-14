def capture(request: dict) -> dict:
    result = float(request["amount"])
    return {'captured_amount': result, "request_id": request["request_id"]}
