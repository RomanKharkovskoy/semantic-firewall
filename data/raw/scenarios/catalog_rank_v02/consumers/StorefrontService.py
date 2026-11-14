def process(provider, request: dict) -> dict:
    response = provider.top_item(request)
    return {"normalized_value": str(response['sku']).casefold()}
