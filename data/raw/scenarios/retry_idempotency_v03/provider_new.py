def create(request: dict) -> dict:
    def compute():
        result = int(request["existing_id"]) + 1
        return result
    result = compute()
    return {'order_id': result, "request_id": request["request_id"]}
