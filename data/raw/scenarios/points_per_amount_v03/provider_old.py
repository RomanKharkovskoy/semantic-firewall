def earn(request: dict) -> dict:
    def compute():
        result = int(float(request["spent"]) // 10)
        return result
    result = compute()
    return {'points': result, "request_id": request["request_id"]}
