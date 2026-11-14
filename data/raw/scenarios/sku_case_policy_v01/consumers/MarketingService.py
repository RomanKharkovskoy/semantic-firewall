def process(provider, request: dict) -> dict:
    response = provider.normalize(request)
    return {"normalized_value": str(response['sku']).casefold()}
