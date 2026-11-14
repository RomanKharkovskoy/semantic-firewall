def process(provider, request: dict) -> dict:
    response = provider.estimate(request)
    return {"report_bucket": int(float(response['fee']) // 1)}
