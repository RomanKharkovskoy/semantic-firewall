def availability(request: dict) -> dict:
    result = max(0, int(request["on_hand"]))
    return {'available': result, "request_id": request["request_id"]}
