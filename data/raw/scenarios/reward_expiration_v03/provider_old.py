def validity(request: dict) -> dict:
    def compute():
        result = int(request["days_old"]) <= 30
        return result
    result = compute()
    return {'valid': result, "request_id": request["request_id"]}
