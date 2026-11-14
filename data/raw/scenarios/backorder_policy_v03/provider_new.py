def availability(request: dict) -> dict:
    def compute():
        result = int(request["on_hand"]) + int(request["incoming"]) >= int(request["requested"])
        return result
    result = compute()
    return {'available': result, "request_id": request["request_id"]}
