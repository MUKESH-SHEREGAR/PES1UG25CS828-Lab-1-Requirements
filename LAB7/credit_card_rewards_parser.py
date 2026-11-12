"""Input-safe parsers for the credit-card rewards lab."""


def mask_card_number(number):
    """Mask a card number, showing no more than its final four ASCII digits.

    Non-string values produce an empty string. Spaces and hyphens are ignored;
    other non-digit characters are discarded before masking.
    """
    if not isinstance(number, str):
        return ""

    digits = "".join(character for character in number if "0" <= character <= "9")
    if not digits:
        return ""
    return "*" * max(0, len(digits) - 4) + digits[-4:]


def parse_transaction(line):
    """Parse ``date,category,amount`` as ``(category, amount)``.

    Malformed input returns the safe sentinel ``("", 0)``.
    """
    if not isinstance(line, str):
        return "", 0

    parts = line.split(",")
    if len(parts) != 3:
        return "", 0

    category = parts[1].strip().lower()
    amount_text = parts[2].strip()
    if not category or not amount_text:
        return "", 0
    try:
        amount = int(amount_text)
    except (ValueError, OverflowError):
        return "", 0
    return category, amount


def parse_statement_total(text):
    """Parse a line such as ``Total: 12,500``; malformed input returns 0."""
    if not isinstance(text, str):
        return 0

    parts = text.split(":", 1)
    if len(parts) != 2 or parts[0].strip().lower() != "total":
        return 0

    amount_text = parts[1].strip().replace(",", "")
    if not amount_text:
        return 0
    try:
        return int(amount_text)
    except (ValueError, OverflowError):
        return 0


def main():
    print("==== Running mask_card_number ====")
    value = input("Enter a card number (e.g. 4111 1111 1111 1234): ")
    print("Masked card number:", mask_card_number(value))

    print("\n==== Running parse_transaction ====")
    value = input("Enter a transaction as DATE,CATEGORY,AMOUNT (e.g. 2026-11-05,dining,1550): ")
    print("Category and amount:", parse_transaction(value))

    print("\n==== Running parse_statement_total ====")
    value = input("Enter the statement total line (e.g. Total: 12,500): ")
    print("Statement total:", parse_statement_total(value))


if __name__ == "__main__":
    main()

