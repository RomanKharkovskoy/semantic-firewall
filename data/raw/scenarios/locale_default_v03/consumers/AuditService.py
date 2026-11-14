def process(provider, request: dict) -> dict:
    response = provider.language(request)
    return {"normalized_value": str(response['locale']).casefold()}
