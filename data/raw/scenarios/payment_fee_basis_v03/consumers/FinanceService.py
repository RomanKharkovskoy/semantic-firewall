def process(provider, request: dict) -> dict:
    response = provider.settle(request)
    return {"report_bucket": int(float(response['net_amount']) // 14)}
