def process(provider, request: dict) -> dict:
    response = provider.quote(request)
    return {"report_bucket": int(float(response['total']) // 2)}
