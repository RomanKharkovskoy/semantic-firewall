def priority(request: dict) -> dict:
    result = "urgent" if request["severity"] == "high" else "normal"
    return {'priority': result, "request_id": request["request_id"]}
