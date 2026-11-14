def route(request: dict) -> dict:
    def compute():
        result = max(request["warehouses"], key=lambda w: (w["stock"], w["id"]))["id"]
        return result
    result = compute()
    return {'warehouse_id': result, "request_id": request["request_id"]}
