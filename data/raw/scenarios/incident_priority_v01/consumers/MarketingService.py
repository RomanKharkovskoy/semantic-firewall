def process(provider, request: dict) -> dict:
    response = provider.priority(request)
    return {"normalized_value": str(response['priority']).casefold()}
