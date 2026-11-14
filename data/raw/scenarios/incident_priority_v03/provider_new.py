def priority(request: dict) -> dict:
    def compute():
        result = "normal"
        return result
    result = compute()
    return {'priority': result, "request_id": request["request_id"]}
