"""Sukanya Samriddhi Yojana, lumpsum MF, inflation, and retirement calculators."""

from __future__ import annotations


def ssy_maturity(
    yearly: float,
    rate: float = 0.082,
    deposit_years: int = 15,
) -> dict:
    """Sukanya Samriddhi Yojana maturity calculator.

    Deposit for 15 years, matures at 21 years. Interest compounds annually.

    Args:
        yearly: Annual deposit (min ₹250, max ₹1.5L).
        rate: Current SSY rate (8.2% for FY 2024-25).
        deposit_years: Years of deposit (max 15, account matures at 21).

    Returns:
        Dict with invested, maturity at 21 years, and interest earned.

    Example:
        >>> ssy_maturity(150000, 0.082, 15)
    """
    yearly = max(min(yearly, 150000), 250)
    balance = 0
    total_invested = 0

    # Deposit phase (15 years)
    for year in range(1, deposit_years + 1):
        balance += yearly
        balance *= (1 + rate)
        total_invested += yearly

    # Growth phase (year 16-21, no deposits, interest continues)
    remaining = 21 - deposit_years
    for _ in range(remaining):
        balance *= (1 + rate)

    return {
        "invested": round(total_invested),
        "maturity": round(balance),
        "interest_earned": round(balance - total_invested),
        "rate": rate,
        "maturity_year": 21,
    }


def lumpsum_maturity(
    amount: float,
    rate: float,
    years: int,
) -> dict:
    """Lumpsum investment future value (one-time MF/equity investment).

    Args:
        amount: One-time investment.
        rate: Expected annual return as decimal.
        years: Investment horizon.

    Returns:
        Dict with invested, returns, maturity.

    Example:
        >>> lumpsum_maturity(500000, 0.12, 10)
    """
    maturity = amount * (1 + rate) ** years
    return {
        "invested": round(amount),
        "returns": round(maturity - amount),
        "maturity": round(maturity),
    }


def future_cost(
    current_cost: float,
    inflation: float = 0.06,
    years: int = 20,
) -> dict:
    """What will something cost in the future due to inflation.

    Example:
        >>> future_cost(50000, 0.06, 20)  # monthly expense today
    """
    future = current_cost * (1 + inflation) ** years
    return {
        "current_cost": round(current_cost),
        "future_cost": round(future),
        "inflation_rate": inflation,
        "years": years,
        "multiplier": round(future / current_cost, 2),
    }


def retirement_corpus(
    monthly_expense: float,
    current_age: int = 30,
    retirement_age: int = 60,
    life_expectancy: int = 85,
    inflation: float = 0.06,
    post_retirement_return: float = 0.07,
) -> dict:
    """How much corpus needed at retirement to sustain expenses.

    Args:
        monthly_expense: Current monthly expense.
        current_age: Current age.
        retirement_age: Planned retirement age.
        life_expectancy: Expected life span.
        inflation: Expected inflation rate.
        post_retirement_return: Expected return on corpus post-retirement.

    Returns:
        Dict with corpus needed, monthly SIP required, and projections.
    """
    years_to_retire = retirement_age - current_age
    years_in_retirement = life_expectancy - retirement_age

    # Future monthly expense at retirement
    future_monthly = monthly_expense * (1 + inflation) ** years_to_retire
    future_annual = future_monthly * 12

    # Corpus needed (present value of annuity at retirement)
    real_return = (1 + post_retirement_return) / (1 + inflation) - 1
    if real_return > 0:
        corpus = future_annual * (1 - (1 + real_return) ** -years_in_retirement) / real_return
    else:
        corpus = future_annual * years_in_retirement

    # Monthly SIP needed to build this corpus (assuming 12% pre-retirement return)
    pre_retirement_return = 0.12
    r = pre_retirement_return / 12
    n = years_to_retire * 12
    if r > 0:
        monthly_sip = corpus / (((1 + r) ** n - 1) / r * (1 + r))
    else:
        monthly_sip = corpus / n

    return {
        "current_monthly_expense": round(monthly_expense),
        "expense_at_retirement": round(future_monthly),
        "corpus_needed": round(corpus),
        "monthly_sip_needed": round(monthly_sip),
        "years_to_retire": years_to_retire,
        "years_in_retirement": years_in_retirement,
    }
