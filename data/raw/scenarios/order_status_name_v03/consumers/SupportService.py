def process(provider, request: dict) -> dict:
    response = provider.summary(request)
    return {"route_prefix": str(response['status']).casefold()[:1]}
