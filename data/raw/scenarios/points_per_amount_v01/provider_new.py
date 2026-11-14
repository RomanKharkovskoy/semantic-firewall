def earn(request: dict) -> dict:
    result = int(float(request["spent"]) // 5)
    return {'points': result, "request_id": request["request_id"]}
