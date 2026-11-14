def process(provider, request: dict) -> dict:
    response = provider.availability(request)
    return {"report_bucket": int(float(response['available']) // 1)}
