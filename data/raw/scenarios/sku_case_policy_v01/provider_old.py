def normalize(request: dict) -> dict:
    result = str(request["sku"]).strip().upper()
    return {'sku': result, "request_id": request["request_id"]}
