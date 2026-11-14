def process(provider, request: dict) -> dict:
    response = provider.calculate(request)
    return {"report_bucket": int(float(response['fee']) // 4)}
