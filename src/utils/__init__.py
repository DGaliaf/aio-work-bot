def is_wallet(line: str) -> bool:
    if len(line) == 42 and line.startswith("0x"):
        return True

    return False


def get_wallets(lines: list[str]) -> list[str]:
    output: list[str] = []

    for line in lines:
        if is_wallet(line):
            output.append(line)

    return output
