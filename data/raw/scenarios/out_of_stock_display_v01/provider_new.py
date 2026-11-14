def visibility(request: dict) -> dict:
    result = int(request["stock"]) > 0 or bool(request["allow_backorder"])
    return {'visible': result, "request_id": request["request_id"]}
