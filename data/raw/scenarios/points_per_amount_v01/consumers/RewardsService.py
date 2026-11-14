def process(provider, request: dict) -> dict:
    response = provider.earn(request)
    return {"report_bucket": int(float(response['points']) // 2)}
