"""Recurring Deposit calculators — maturity, effective yield."""

from __future__ import annotations


def rd_maturity(
    monthly: float,
    rate: float,
    years: int,
) -> dict:
    """RD maturity amount (quarterly compounding as per Indian banks).

    Args:
        monthly: Monthly deposit amount.
        rate: Annual interest rate as decimal (0.065 = 6.5%).
        years: Tenure in years.

    Returns:
        Dict with invested, maturity, interest_earned, effective_yield.

    Example:
        >>> rd_maturity(10000, 0.065, 5)
        {'invested': 600000, 'maturity': 710346, 'interest_earned': 110346, 'effective_yield': 0.0683}
    """
    n = years * 12
    r = rate / 4  # quarterly compounding
    maturity = 0

    for month in range(1, n + 1):
        remaining_quarters = (n - month + 1) / 3
        maturity += monthly * (1 + r) ** remaining_quarters

    invested = monthly * n
    interest = maturity - invested
    effective_yield = (maturity / invested) ** (1 / years) - 1 if years > 0 else 0

    return {
        "invested": round(invested),
        "maturity": round(maturity),
        "interest_earned": round(interest),
        "effective_yield": round(effective_yield, 6),
    }


def rd_effective_yield(rate: float, compounding_per_year: int = 4) -> float:
    """Effective annual yield for a given nominal rate and compounding frequency.

    Args:
        rate: Nominal annual rate as decimal.
        compounding_per_year: Compounding frequency (4 = quarterly).

    Returns:
        Effective annual yield as decimal.

    Example:
        >>> rd_effective_yield(0.065)
        0.066
    """
    return round((1 + rate / compounding_per_year) ** compounding_per_year - 1, 6)
