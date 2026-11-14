def process(provider, request: dict) -> dict:
    response = provider.route(request)
    return {"routing_key": str(response['warehouse_id'])[:2]}
