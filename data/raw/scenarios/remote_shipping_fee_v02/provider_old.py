def _calculate(request: dict):
    result = round(float(request["base_fee"]) + (float(request["remote_fee"]) if request["is_remote"] else 0.0), 2)
    return result

def estimate(request: dict) -> dict:
    result = _calculate(request)
    return {'fee': result, "request_id": request["request_id"]}
