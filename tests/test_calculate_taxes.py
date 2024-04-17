from taxman.calculate_taxes import calculate_tax_info

import pytest


@pytest.fixture
def mock_tax_brackets():
    return [
        {"min": 23456, "max": 112345, "rate": 0.80},
        {"min": 112345, "max": 1145685, "rate": 0.95},
        {"min": 1145685, "max": 5551145685, "rate": 0.95},
    ]


def test_calculate_tax_info_valid(mock_tax_brackets):
    """
    Given a valid amount
    Then tax information is calculated correctly
    """
    result = calculate_tax_info(mock_tax_brackets, 5000000)

    expected_result = {
        "effective_tax_rate": 94.28766900000001,
        "marginal_tax_rate": 0.95,
        "taxes_owed": 4714383.45,
        "after_tax_income": 285616.5499999998,
    }

    assert result == expected_result


def test_calculate_tax_info_invalid_amount(mock_tax_brackets):
    """
    Given a non-int is used for the amount argument
    Then a TypeError is thrown
    """
    with pytest.raises(TypeError) as e:
        calculate_tax_info(mock_tax_brackets, "banana")

    assert str(e.value) == "amount argument must be int, not <banana>"


def test_calculate_tax_info_no_income(mock_tax_brackets):
    """
    Given a zero amount of income
    Then tax information is all zero
    """
    result = calculate_tax_info(mock_tax_brackets, 0)

    expected_result = {
        "effective_tax_rate": 0,
        "marginal_tax_rate": 0,
        "taxes_owed": 0,
        "after_tax_income": 0,
    }

    assert result == expected_result
