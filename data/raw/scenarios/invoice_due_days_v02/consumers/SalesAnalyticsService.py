def process(provider, request: dict) -> dict:
    response = provider.deadline(request)
    return {"observed": response['due_date'], "reference": response["request_id"]}
