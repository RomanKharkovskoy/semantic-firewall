def process(provider, request: dict) -> dict:
    response = provider.priority(request)
    return {"routing_key": str(response['priority'])[:2]}
