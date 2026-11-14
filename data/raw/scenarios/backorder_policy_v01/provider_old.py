def availability(request: dict) -> dict:
    result = int(request["on_hand"]) >= int(request["requested"])
    return {'available': result, "request_id": request["request_id"]}
