def validity(request: dict) -> dict:
    result = int(request["days_old"]) <= 30
    return {'valid': result, "request_id": request["request_id"]}
