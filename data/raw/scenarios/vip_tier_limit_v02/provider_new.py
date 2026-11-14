def _calculate(request: dict):
    result = "VIP" if int(request["points"]) > int(request["threshold"]) else "STANDARD"
    return result

def tier(request: dict) -> dict:
    result = _calculate(request)
    return {'tier': result, "request_id": request["request_id"]}
