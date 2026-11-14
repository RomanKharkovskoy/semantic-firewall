def process(provider, request: dict) -> dict:
    response = provider.summary(request)
    return {"normalized_value": str(response['status']).casefold()}
