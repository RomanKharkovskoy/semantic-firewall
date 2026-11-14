def process(provider, request: dict) -> dict:
    response = provider.capture(request)
    return {"report_bucket": int(float(response['captured_amount']) // 1)}
