def normalize(request: dict) -> dict:
    def compute():
        result = str(request["sku"]).strip().upper()
        return result
    result = compute()
    return {'sku': result, "request_id": request["request_id"]}
