def summary(request: dict) -> dict:
    result = "PAID" if request["captured"] else "PENDING"
    return {'status': result, "request_id": request["request_id"]}
