def process(provider, request: dict) -> dict:
    response = provider.deadline(request)
    return {"normalized_value": str(response['due_date']).casefold()}
