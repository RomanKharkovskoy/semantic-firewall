def process(provider, request: dict) -> dict:
    response = provider.language(request)
    return {"routing_key": str(response['locale'])[:2]}
