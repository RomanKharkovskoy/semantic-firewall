def route(request: dict) -> dict:
    def compute():
        result = min(request["warehouses"], key=lambda w: (w["distance_km"], w["id"]))["id"]
        return result
    result = compute()
    return {'warehouse_id': result, "request_id": request["request_id"]}
