def refund(request: dict) -> dict:
    result = round(float(request["item_amount"]) + float(request["delivery_fee"]), 2)
    return {'refund': result, "request_id": request["request_id"]}
