def process(provider, request: dict) -> dict:
    response = provider.tier(request)
    return {"normalized_value": str(response['tier']).casefold()}
