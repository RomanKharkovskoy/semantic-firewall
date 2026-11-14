def route(request: dict) -> dict:
    result = max(request["warehouses"], key=lambda w: (w["stock"], w["id"]))["id"]
    return {'warehouse_id': result, "request_id": request["request_id"]}
