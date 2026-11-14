def top_item(request: dict) -> dict:
    result = sorted(request["items"], key=lambda item: (-item["score"], item["sku"]))[0]["sku"]
    return {'sku': result, "request_id": request["request_id"]}
