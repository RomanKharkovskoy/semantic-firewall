def priority(request: dict) -> dict:
    result = "normal"
    return {'priority': result, "request_id": request["request_id"]}
