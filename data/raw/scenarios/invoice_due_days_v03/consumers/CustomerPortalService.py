def process(provider, request: dict) -> dict:
    response = provider.deadline(request)
    chosen = response['due_date'] if request.get("use_result", False) else "not_requested"
    return {"selected": chosen}
