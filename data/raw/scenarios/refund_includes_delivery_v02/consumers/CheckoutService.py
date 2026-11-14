def process(provider, request: dict) -> dict:
    response = provider.refund(request)
    return {"report_bucket": int(float(response['refund']) // 20)}
