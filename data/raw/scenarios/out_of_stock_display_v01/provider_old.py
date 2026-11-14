def visibility(request: dict) -> dict:
    result = int(request["stock"]) > 0
    return {'visible': result, "request_id": request["request_id"]}
