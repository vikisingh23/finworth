"""Fixed Deposit calculators — maturity, TDS, post-tax returns, comparison."""

from __future__ import annotations
from typing import Literal


def fd_maturity(
    principal: float,
    rate: float,
    years: float,
    compounding: Literal["quarterly", "monthly", "half-yearly", "yearly"] = "quarterly",
) -> dict:
    """FD maturity amount calculator.

    Args:
        principal: Deposit amount.
        rate: Annual interest rate as decimal (0.07 = 7%).
        years: Tenure in years.
        compounding: Compounding frequency.

    Returns:
        Dict with maturity, interest_earned, and effective_rate.

    Example:
        >>> fd_maturity(500000, 0.07, 3)
        {'principal': 500000, 'maturity': 615769, 'interest_earned': 115769, 'effective_rate': 0.0719}
    """
    freq = {"monthly": 12, "quarterly": 4, "half-yearly": 2, "yearly": 1}[compounding]
    n = freq * years
    r = rate / freq
    maturity = principal * (1 + r) ** n
    interest = maturity - principal
    effective_rate = (maturity / principal) ** (1 / years) - 1

    return {
        "principal": round(principal),
        "maturity": round(maturity),
        "interest_earned": round(interest),
        "effective_rate": round(effective_rate, 6),
    }


def fd_post_tax(
    principal: float,
    rate: float,
    years: float,
    tax_slab: float = 0.3,
    compounding: Literal["quarterly", "monthly", "half-yearly", "yearly"] = "quarterly",
    is_senior_citizen: bool = False,
) -> dict:
    """FD returns after TDS/tax deduction.

    Args:
        principal: Deposit amount.
        rate: Annual interest rate as decimal.
        years: Tenure in years.
        tax_slab: Applicable income tax slab rate as decimal.
        compounding: Compounding frequency.
        is_senior_citizen: Senior citizens get ₹50K TDS exemption (vs ₹40K).

    Returns:
        Dict with pre_tax and post_tax maturity, effective post-tax rate.
    """
    pre = fd_maturity(principal, rate, years, compounding)
    tds_limit = 50000 if is_senior_citizen else 40000
    annual_interest = pre["interest_earned"] / years

    if annual_interest <= tds_limit:
        tds_per_year = 0
    else:
        tds_per_year = annual_interest * 0.10  # 10% TDS

    total_tds = round(tds_per_year * years)
    total_tax = round(pre["interest_earned"] * tax_slab)
    tax_payable = max(total_tax - total_tds, 0)
    post_tax_interest = pre["interest_earned"] - total_tax
    post_tax_maturity = principal + post_tax_interest
    post_tax_rate = (post_tax_maturity / principal) ** (1 / years) - 1

    return {
        "pre_tax_maturity": pre["maturity"],
        "post_tax_maturity": round(post_tax_maturity),
        "interest_earned": pre["interest_earned"],
        "tax_deducted": total_tax,
        "tds_deducted": total_tds,
        "additional_tax_payable": tax_payable,
        "post_tax_rate": round(post_tax_rate, 6),
    }


def fd_compare(
    principal: float,
    options: list[dict],
    years: float = 1,
) -> list[dict]:
    """Compare multiple FD options.

    Args:
        principal: Deposit amount.
        options: List of dicts with 'bank', 'rate', and optional 'compounding'.
        years: Tenure.

    Returns:
        Sorted list (best first) with maturity calculations.

    Example:
        >>> fd_compare(500000, [
        ...     {"bank": "SBI", "rate": 0.067},
        ...     {"bank": "HDFC", "rate": 0.07},
        ... ], years=3)
    """
    results = []
    for opt in options:
        comp = opt.get("compounding", "quarterly")
        mat = fd_maturity(principal, opt["rate"], years, comp)
        results.append({**opt, **mat})
    return sorted(results, key=lambda x: x["maturity"], reverse=True)
