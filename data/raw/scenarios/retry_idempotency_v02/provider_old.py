def _calculate(request: dict):
    result = int(request["existing_id"]) if request["is_retry"] else int(request["existing_id"]) + 1
    return result

def create(request: dict) -> dict:
    result = _calculate(request)
    return {'order_id': result, "request_id": request["request_id"]}
