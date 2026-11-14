def availability(request: dict) -> dict:
    def compute():
        result = max(0, int(request["on_hand"]) - int(request["reserved"]))
        return result
    result = compute()
    return {'available': result, "request_id": request["request_id"]}
