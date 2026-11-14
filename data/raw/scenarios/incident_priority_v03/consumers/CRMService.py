def process(provider, request: dict) -> dict:
    response = provider.priority(request)
    return {"route_prefix": str(response['priority']).casefold()[:1]}
