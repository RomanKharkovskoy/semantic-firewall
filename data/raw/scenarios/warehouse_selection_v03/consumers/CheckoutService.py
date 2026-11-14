def process(provider, request: dict) -> dict:
    response = provider.route(request)
    return {"normalized_value": str(response['warehouse_id']).casefold()}
