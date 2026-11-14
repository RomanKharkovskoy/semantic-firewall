def process(provider, request: dict) -> dict:
    response = provider.deadline(request)
    return {"route_prefix": str(response['due_date']).casefold()[:1]}
