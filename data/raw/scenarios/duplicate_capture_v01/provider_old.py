def capture(request: dict) -> dict:
    result = 0.0 if request["was_captured"] else float(request["amount"])
    return {'captured_amount': result, "request_id": request["request_id"]}
