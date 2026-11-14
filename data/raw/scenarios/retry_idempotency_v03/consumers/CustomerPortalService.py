def process(provider, request: dict) -> dict:
    response = provider.create(request)
    return {"report_bucket": int(float(response['order_id']) // 60)}
