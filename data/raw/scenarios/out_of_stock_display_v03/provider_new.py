def visibility(request: dict) -> dict:
    def compute():
        result = int(request["stock"]) > 0 or bool(request["allow_backorder"])
        return result
    result = compute()
    return {'visible': result, "request_id": request["request_id"]}
