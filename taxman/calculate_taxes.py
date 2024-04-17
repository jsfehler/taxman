from decimal import Decimal
from typing import Mapping


def calculate_tax_info(
    tax_brackets: list[dict[str, int]],
    amount: int,
) -> Mapping[str, Decimal]:
    """Calaculate tax information.

    Arguments:
        tax_brackets: Collection of min, max, rate values for tax brackets
        amount: The amount to calculate taxes for.

    Returns:
        dict - Taxation information.
    """
    if not isinstance(amount, (int, float)):
        raise TypeError(f"amount argument must be int or float, not <{amount}>")

    # When you're dealing with cash money, always use Decimal. float was not
    # designed for extremely precise calculations.
    decimal_amount = Decimal(amount)

    rv: Mapping[str, Decimal] = {
        "effective_tax_rate": Decimal(0.0),
        "marginal_tax_rate": Decimal(0.0),
        "taxes_owed": Decimal(0.0),
        "after_tax_income": Decimal(0.0),
    }

    if decimal_amount == 0:
        return rv

    for bracket in tax_brackets:
        _min = Decimal(bracket["min"])
        _max = Decimal(bracket.get("max", decimal_amount))
        rate = Decimal(bracket["rate"])
        rv["marginal_tax_rate"] = rate

        if decimal_amount >= _max:
            taxable_amount_in_bracket = _max - _min
            rv["taxes_owed"] += taxable_amount_in_bracket * rate
        else:
            taxable_amount_in_bracket = decimal_amount - _min
            rv["taxes_owed"] += taxable_amount_in_bracket * rate
            break

    rv["effective_tax_rate"] = (rv["taxes_owed"] / decimal_amount) * 100
    rv["after_tax_income"] = decimal_amount - rv["taxes_owed"]

    return rv
