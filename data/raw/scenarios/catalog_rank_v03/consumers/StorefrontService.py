def process(provider, request: dict) -> dict:
    response = provider.top_item(request)
    return {"route_prefix": str(response['sku']).casefold()[:1]}
