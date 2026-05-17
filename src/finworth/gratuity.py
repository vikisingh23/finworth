"""Gratuity calculator — Payment of Gratuity Act, 1972."""

from __future__ import annotations
from typing import Literal


def gratuity(
    basic_da: float,
    years_of_service: float,
    employee_type: Literal["private", "government", "fixed-term"] = "private",
) -> dict:
    """Gratuity calculation under Payment of Gratuity Act.

    Args:
        basic_da: Last drawn Basic + DA (monthly).
        years_of_service: Total years of service (min 5 years to be eligible).
        employee_type: 'private' (15/26), 'government' (15/30), or 'fixed-term' (pro-rata, no 5yr min per Labour Code 2025).

    Returns:
        Dict with eligible, gratuity_amount, tax_exempt, and taxable.

    Example:
        >>> gratuity(80000, 10)
        >>> gratuity(50000, 2, "fixed-term")
    """
    # Labour Code: fixed-term workers get pro-rata gratuity (no 5-year minimum)
    eligible = True if employee_type == "fixed-term" else years_of_service >= 5
    completed_years = int(years_of_service + 0.5)  # round to nearest year (>6 months = 1 year)

    if employee_type == "government":
        amount = basic_da * 15 * completed_years / 30
    else:
        amount = basic_da * 15 * completed_years / 26

    # Tax exemption: least of (a) actual gratuity, (b) ₹20L, (c) formula amount
    max_exempt = 2000000  # ₹20L limit
    tax_exempt = min(amount, max_exempt)
    taxable = max(amount - max_exempt, 0)

    return {
        "eligible": eligible,
        "basic_da_monthly": round(basic_da),
        "years_of_service": round(years_of_service, 1),
        "completed_years": completed_years,
        "gratuity_amount": round(amount),
        "tax_exempt": round(tax_exempt),
        "taxable": round(taxable),
    }
