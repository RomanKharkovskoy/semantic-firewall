def validity(request: dict) -> dict:
    result = int(request["days_old"]) <= 14
    return {'valid': result, "request_id": request["request_id"]}
