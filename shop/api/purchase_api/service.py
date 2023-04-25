from purchase.models import OrderItem


def is_payment_valid(card_number: str):
    return card_number[-1] != '0' and int(card_number) % 2 == 0


def check_stock_availability(purchases: list[OrderItem]):
    """
    Check if product stock more than quantity or equal to quantity
    Return errors if not
    """
    errors = []
    for purchase in purchases:
        if purchase.product.stock < purchase.quantity:
            errors.append(f'not enough {purchase.product.title}')

    return errors


def reduce_product_stock_with_purchase_quantity(purchases: list[OrderItem]):
    """"""
    for purchase in purchases:
        purchase.product.stock -= purchase.quantity
