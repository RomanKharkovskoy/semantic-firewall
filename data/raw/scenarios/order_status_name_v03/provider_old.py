def summary(request: dict) -> dict:
    def compute():
        result = "PAID" if request["captured"] else "PENDING"
        return result
    result = compute()
    return {'status': result, "request_id": request["request_id"]}
