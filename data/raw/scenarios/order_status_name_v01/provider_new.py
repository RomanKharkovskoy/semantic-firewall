def summary(request: dict) -> dict:
    result = "COMPLETE" if request["captured"] else "PENDING"
    return {'status': result, "request_id": request["request_id"]}
