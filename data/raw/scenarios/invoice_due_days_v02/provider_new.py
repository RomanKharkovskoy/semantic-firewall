from datetime import date, timedelta

def _calculate(request: dict):
    result = (date.fromisoformat(request["issued_on"]) + timedelta(days=14)).isoformat()
    return result

def deadline(request: dict) -> dict:
    result = _calculate(request)
    return {'due_date': result, "request_id": request["request_id"]}
