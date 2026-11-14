def dispatch(request: dict) -> dict:
    result = True
    return {'should_send': result, "request_id": request["request_id"]}
