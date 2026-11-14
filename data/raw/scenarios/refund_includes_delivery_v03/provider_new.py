def refund(request: dict) -> dict:
    def compute():
        result = round(float(request["item_amount"]) + float(request["delivery_fee"]), 2)
        return result
    result = compute()
    return {'refund': result, "request_id": request["request_id"]}
