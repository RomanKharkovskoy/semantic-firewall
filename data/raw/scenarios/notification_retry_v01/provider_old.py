def dispatch(request: dict) -> dict:
    result = not bool(request["already_sent"])
    return {'should_send': result, "request_id": request["request_id"]}
