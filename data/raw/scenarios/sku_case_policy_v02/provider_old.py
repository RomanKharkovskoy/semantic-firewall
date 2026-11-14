def _calculate(request: dict):
    result = str(request["sku"]).strip().upper()
    return result

def normalize(request: dict) -> dict:
    result = _calculate(request)
    return {'sku': result, "request_id": request["request_id"]}
