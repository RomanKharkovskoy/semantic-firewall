def dispatch(request: dict) -> dict:
    def compute():
        result = not bool(request["already_sent"])
        return result
    result = compute()
    return {'should_send': result, "request_id": request["request_id"]}
