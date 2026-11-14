def process(provider, request: dict) -> dict:
    response = provider.normalize(request)
    return {"route_prefix": str(response['sku']).casefold()[:1]}
