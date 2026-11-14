def normalize(request: dict) -> dict:
    result = str(request["sku"]).strip().lower()
    return {'sku': result, "request_id": request["request_id"]}
