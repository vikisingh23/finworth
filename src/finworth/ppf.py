"""Public Provident Fund calculator — maturity, yearly breakdown."""

from __future__ import annotations


def ppf_maturity(
    yearly: float,
    rate: float = 0.071,
    years: int = 15,
) -> dict:
    """PPF maturity calculator (annual compounding, 15-year lock-in).

    Args:
        yearly: Annual contribution (max ₹1.5L).
        rate: Current PPF interest rate as decimal (default 7.1% for FY 2024-25).
        years: Duration (min 15, extendable in 5-year blocks).

    Returns:
        Dict with invested, interest_earned, maturity, and yearly_breakdown.

    Example:
        >>> ppf_maturity(150000, 0.071, 15)
    """
    yearly = min(yearly, 150000)  # PPF max ₹1.5L/year
    balance = 0
    total_invested = 0
    breakdown = []

    for year in range(1, years + 1):
        balance += yearly
        interest = balance * rate
        balance += interest
        total_invested += yearly
        breakdown.append({
            "year": year,
            "deposit": round(yearly),
            "interest": round(interest),
            "balance": round(balance),
        })

    return {
        "invested": round(total_invested),
        "interest_earned": round(balance - total_invested),
        "maturity": round(balance),
        "rate": rate,
        "years": years,
        "yearly_breakdown": breakdown,
    }


def ppf_extension(
    current_balance: float,
    yearly: float = 0,
    rate: float = 0.071,
    extension_years: int = 5,
    with_contribution: bool = True,
) -> dict:
    """PPF extension after 15 years (5-year blocks).

    Args:
        current_balance: Balance at end of 15 years.
        yearly: Annual contribution during extension (0 if without contribution).
        rate: Interest rate.
        extension_years: Extension period (must be multiple of 5).
        with_contribution: Whether to contribute during extension.

    Returns:
        Dict with final balance and breakdown.
    """
    if not with_contribution:
        yearly = 0

    balance = current_balance
    total_added = 0
    breakdown = []

    for year in range(1, extension_years + 1):
        balance += yearly
        interest = balance * rate
        balance += interest
        total_added += yearly
        breakdown.append({
            "year": year,
            "deposit": round(yearly),
            "interest": round(interest),
            "balance": round(balance),
        })

    return {
        "opening_balance": round(current_balance),
        "additional_invested": round(total_added),
        "interest_earned": round(balance - current_balance - total_added),
        "final_balance": round(balance),
        "yearly_breakdown": breakdown,
    }
