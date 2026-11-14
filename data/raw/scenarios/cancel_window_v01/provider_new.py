def cancellable(request: dict) -> dict:
    result = float(request["hours_since_order"]) < 24
    return {'allowed': result, "request_id": request["request_id"]}
