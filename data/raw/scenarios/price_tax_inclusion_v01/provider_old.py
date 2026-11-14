def quote(request: dict) -> dict:
    result = round(float(request["subtotal"]), 2)
    return {'total': result, "request_id": request["request_id"]}
