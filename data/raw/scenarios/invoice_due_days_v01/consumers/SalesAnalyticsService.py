def process(provider, request: dict) -> dict:
    response = provider.deadline(request)
    return {"routing_key": str(response['due_date'])[:2]}
