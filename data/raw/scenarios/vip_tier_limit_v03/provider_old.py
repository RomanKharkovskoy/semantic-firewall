def tier(request: dict) -> dict:
    def compute():
        result = "VIP" if int(request["points"]) >= int(request["threshold"]) else "STANDARD"
        return result
    result = compute()
    return {'tier': result, "request_id": request["request_id"]}
