def process(provider, request: dict) -> dict:
    response = provider.summary(request)
    return {"routing_key": str(response['status'])[:2]}
