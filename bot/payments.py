"""Placeholder Mercado Pago integration."""


def create_payment(amount: float, description: str) -> str:
    """Return a dummy payment link."""
    return f'https://www.mercadopago.com.br/pay?amount={amount}&desc={description}'
