def process(provider, request: dict) -> dict:
    response = provider.normalize(request)
    return {"routing_key": str(response['sku'])[:2]}
