def settle(request: dict) -> dict:
    def compute():
        result = round((float(request["gross"]) - float(request["fixed_fee"])) * (1 - float(request["rate"])), 2)
        return result
    result = compute()
    return {'net_amount': result, "request_id": request["request_id"]}
