
def is_wallet(line: str) -> bool:
    if len(line) == 42 and line.startswith("0x"):
        return True

    return False
