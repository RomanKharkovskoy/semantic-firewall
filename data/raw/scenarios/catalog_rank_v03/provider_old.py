def top_item(request: dict) -> dict:
    def compute():
        result = sorted(request["items"], key=lambda item: (-item["score"], item["sku"]))[0]["sku"]
        return result
    result = compute()
    return {'sku': result, "request_id": request["request_id"]}
