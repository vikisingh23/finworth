"""EMI calculator — home loan, personal loan, car loan with amortization."""

from __future__ import annotations
from typing import Literal


def emi(
    principal: float,
    rate: float,
    years: int,
) -> dict:
    """EMI (Equated Monthly Installment) calculator.

    Args:
        principal: Loan amount.
        rate: Annual interest rate as decimal (0.085 = 8.5%).
        years: Loan tenure in years.

    Returns:
        Dict with emi, total_payment, total_interest, and interest_to_principal_ratio.

    Example:
        >>> emi(5000000, 0.085, 20)
        {'emi': 43391, 'total_payment': 10413816, 'total_interest': 5413816}
    """
    n = years * 12
    r = rate / 12

    if r == 0:
        monthly = principal / n
    else:
        monthly = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

    total = monthly * n
    interest = total - principal

    return {
        "principal": round(principal),
        "emi": round(monthly),
        "total_payment": round(total),
        "total_interest": round(interest),
        "interest_to_principal": round(interest / principal, 2) if principal > 0 else 0,
        "tenure_months": n,
        "rate": rate,
    }


def emi_amortization(
    principal: float,
    rate: float,
    years: int,
) -> list[dict]:
    """Year-wise amortization schedule.

    Returns:
        List of yearly breakdowns with principal_paid, interest_paid, and balance.
    """
    n = years * 12
    r = rate / 12
    if r == 0:
        monthly = principal / n
    else:
        monthly = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

    balance = principal
    schedule = []

    for year in range(1, years + 1):
        yearly_principal = 0
        yearly_interest = 0
        for _ in range(12):
            interest_part = balance * r
            principal_part = monthly - interest_part
            balance -= principal_part
            yearly_principal += principal_part
            yearly_interest += interest_part

        schedule.append({
            "year": year,
            "principal_paid": round(yearly_principal),
            "interest_paid": round(yearly_interest),
            "total_paid": round(yearly_principal + yearly_interest),
            "balance": round(max(balance, 0)),
        })

    return schedule


def emi_prepayment_impact(
    principal: float,
    rate: float,
    years: int,
    prepayment: float,
    prepay_after_months: int = 12,
    strategy: Literal["reduce_tenure", "reduce_emi"] = "reduce_tenure",
) -> dict:
    """Impact of lump-sum prepayment on loan.

    Args:
        principal: Original loan amount.
        rate: Annual interest rate.
        years: Original tenure.
        prepayment: Lump-sum prepayment amount.
        prepay_after_months: When to prepay (months from start).
        strategy: 'reduce_tenure' or 'reduce_emi'.

    Returns:
        Dict comparing original vs post-prepayment scenarios.
    """
    original = emi(principal, rate, years)
    r = rate / 12
    monthly = original["emi"]

    # Calculate balance at prepayment point
    balance = principal
    for _ in range(prepay_after_months):
        interest = balance * r
        balance = balance + interest - monthly

    new_balance = balance - prepayment
    if new_balance <= 0:
        return {
            "original": original,
            "loan_closed": True,
            "interest_saved": round(original["total_interest"]),
        }

    if strategy == "reduce_tenure":
        new_emi = monthly
        # Calculate new tenure
        if r > 0:
            import math
            new_months = math.ceil(math.log(new_emi / (new_emi - new_balance * r)) / math.log(1 + r))
        else:
            new_months = math.ceil(new_balance / new_emi)
        new_total = new_emi * new_months + monthly * prepay_after_months
        months_saved = (years * 12) - (prepay_after_months + new_months)
    else:
        new_months = (years * 12) - prepay_after_months
        if r == 0:
            new_emi = new_balance / new_months
        else:
            new_emi = new_balance * r * (1 + r) ** new_months / ((1 + r) ** new_months - 1)
        new_total = new_emi * new_months + monthly * prepay_after_months
        months_saved = 0

    interest_saved = original["total_payment"] - (new_total + prepayment)

    return {
        "original_emi": original["emi"],
        "original_tenure_months": years * 12,
        "original_total_interest": original["total_interest"],
        "prepayment": round(prepayment),
        "new_emi": round(new_emi),
        "new_tenure_months": prepay_after_months + (new_months if strategy == "reduce_tenure" else (years * 12) - prepay_after_months),
        "months_saved": months_saved,
        "interest_saved": round(interest_saved),
        "strategy": strategy,
    }
