def _calculate(request: dict):
    result = sorted(request["items"], key=lambda item: (item["title"], item["sku"]))[0]["sku"]
    return result

def top_item(request: dict) -> dict:
    result = _calculate(request)
    return {'sku': result, "request_id": request["request_id"]}
