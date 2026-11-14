def process(provider, request: dict) -> dict:
    response = provider.tier(request)
    return {"routing_key": str(response['tier'])[:2]}
