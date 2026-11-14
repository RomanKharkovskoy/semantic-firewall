def process(provider, request: dict) -> dict:
    response = provider.availability(request)
    return {"policy_triggered": float(response['available']) >= 4.0}
