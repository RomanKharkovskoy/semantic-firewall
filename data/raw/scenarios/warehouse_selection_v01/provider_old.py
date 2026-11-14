def route(request: dict) -> dict:
    result = min(request["warehouses"], key=lambda w: (w["distance_km"], w["id"]))["id"]
    return {'warehouse_id': result, "request_id": request["request_id"]}
