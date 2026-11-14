def process(provider, request: dict) -> dict:
    response = provider.tier(request)
    return {"route_prefix": str(response['tier']).casefold()[:1]}
