def process(provider, request: dict) -> dict:
    response = provider.calculate(request)
    return {"observed": response['fee'], "reference": response["request_id"]}
