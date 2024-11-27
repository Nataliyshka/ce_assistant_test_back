def check_status_code(code: int) -> bool:
    if code >= 200 and code < 400:
        return True
    
    return False