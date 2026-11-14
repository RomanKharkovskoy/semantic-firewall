def language(request: dict) -> dict:
    def compute():
        result = request.get("locale") or "ru"
        return result
    result = compute()
    return {'locale': result, "request_id": request["request_id"]}
