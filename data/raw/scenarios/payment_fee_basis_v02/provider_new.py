def _calculate(request: dict):
    result = round((float(request["gross"]) - float(request["fixed_fee"])) * (1 - float(request["rate"])), 2)
    return result

def settle(request: dict) -> dict:
    result = _calculate(request)
    return {'net_amount': result, "request_id": request["request_id"]}
