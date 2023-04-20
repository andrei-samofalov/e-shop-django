def is_payment_valid(card_number: str):
    return card_number[-1] != '0' and int(card_number) % 2 == 0
