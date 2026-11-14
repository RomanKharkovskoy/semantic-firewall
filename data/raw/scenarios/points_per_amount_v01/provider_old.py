def earn(request: dict) -> dict:
    result = int(float(request["spent"]) // 10)
    return {'points': result, "request_id": request["request_id"]}
