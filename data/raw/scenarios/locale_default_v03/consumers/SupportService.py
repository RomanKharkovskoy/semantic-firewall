def process(provider, request: dict) -> dict:
    response = provider.language(request)
    return {"route_prefix": str(response['locale']).casefold()[:1]}
