def tier(request: dict) -> dict:
    result = "VIP" if int(request["points"]) > int(request["threshold"]) else "STANDARD"
    return {'tier': result, "request_id": request["request_id"]}
