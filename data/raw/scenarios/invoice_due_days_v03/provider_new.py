from datetime import date, timedelta

def deadline(request: dict) -> dict:
    def compute():
        result = (date.fromisoformat(request["issued_on"]) + timedelta(days=14)).isoformat()
        return result
    result = compute()
    return {'due_date': result, "request_id": request["request_id"]}
