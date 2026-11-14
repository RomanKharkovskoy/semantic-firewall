def process(provider, request: dict) -> dict:
    response = provider.route(request)
    return {"route_prefix": str(response['warehouse_id']).casefold()[:1]}
