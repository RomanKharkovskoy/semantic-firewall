def process(provider, request: dict) -> dict:
    response = provider.settle(request)
    return {"observed": response['net_amount'], "reference": response["request_id"]}
