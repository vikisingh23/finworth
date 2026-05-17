"""Salary calculators — HRA exemption, CTC to in-hand, salary breakup."""

from __future__ import annotations
from typing import Literal


def hra_exemption(
    basic: float,
    hra_received: float,
    rent_paid: float,
    metro: bool = True,
) -> dict:
    """HRA tax exemption (Section 10(13A)).

    Exempt = least of:
    1. Actual HRA received
    2. 50% of basic (metro) or 40% (non-metro)
    3. Rent paid - 10% of basic

    Args:
        basic: Monthly basic salary.
        hra_received: Monthly HRA received.
        rent_paid: Monthly rent paid.
        metro: True for Delhi/Mumbai/Kolkata/Chennai.

    Returns:
        Dict with exempt amount, taxable HRA, and breakdown.

    Example:
        >>> hra_exemption(50000, 20000, 25000, metro=True)
    """
    annual_basic = basic * 12
    annual_hra = hra_received * 12
    annual_rent = rent_paid * 12

    actual_hra = annual_hra
    percent_of_basic = annual_basic * (0.50 if metro else 0.40)
    rent_minus_10 = max(annual_rent - annual_basic * 0.10, 0)

    exempt = min(actual_hra, percent_of_basic, rent_minus_10)
    taxable = annual_hra - exempt

    return {
        "annual_hra_received": round(annual_hra),
        "exempt_amount": round(exempt),
        "taxable_hra": round(taxable),
        "breakdown": {
            "actual_hra": round(actual_hra),
            "50_or_40_percent_basic": round(percent_of_basic),
            "rent_minus_10_percent_basic": round(rent_minus_10),
        },
    }


def ctc_to_inhand(
    ctc: float,
    basic_percent: float = 0.40,
    hra_percent: float = 0.20,
    special_allowance: bool = True,
    employer_pf: bool = True,
    employer_pf_on_ctc: bool = False,
    professional_tax: float = 2400,
    regime: Literal["old", "new"] = "new",
) -> dict:
    """CTC to monthly in-hand salary calculator (legacy structure).

    Args:
        ctc: Annual CTC.
        basic_percent: Basic as % of CTC (typically 40-50%).
        hra_percent: HRA as % of CTC (typically 20-25%).
        special_allowance: Whether remaining goes to special allowance.
        employer_pf: Whether employer contributes to PF.
        employer_pf_on_ctc: If True, PF is part of CTC; if False, it's additional.
        professional_tax: Annual professional tax (₹2400 in most states).
        regime: Tax regime for estimation.

    Returns:
        Dict with full salary breakup and monthly in-hand.
    """
    basic = ctc * basic_percent
    hra = ctc * hra_percent

    # Employer PF: 12% of basic, capped at ₹1800/month (₹15K basic cap)
    pf_basic = min(basic, 180000)  # ₹15K/month cap
    employee_pf = pf_basic * 0.12
    employer_pf_amount = pf_basic * 0.12 if employer_pf else 0

    # Gratuity: 4.81% of basic (15/26 * 12)
    gratuity_annual = basic * 0.0481

    if employer_pf_on_ctc:
        remaining = ctc - basic - hra - employer_pf_amount - gratuity_annual
    else:
        remaining = ctc - basic - hra - gratuity_annual

    special = max(remaining, 0) if special_allowance else 0

    gross_salary = basic + hra + special
    total_deductions = employee_pf + professional_tax

    # Rough tax estimate
    from finworth.tax import income_tax_slab
    tax_info = income_tax_slab(gross_salary, regime)
    monthly_tax = tax_info["total_tax"] / 12

    net_monthly = (gross_salary - total_deductions) / 12 - monthly_tax

    return {
        "ctc": round(ctc),
        "basic_annual": round(basic),
        "hra_annual": round(hra),
        "special_allowance_annual": round(special),
        "employer_pf_annual": round(employer_pf_amount),
        "gratuity_annual": round(gratuity_annual),
        "gross_salary_annual": round(gross_salary),
        "employee_pf_annual": round(employee_pf),
        "professional_tax_annual": round(professional_tax),
        "estimated_tax_annual": round(tax_info["total_tax"]),
        "net_annual": round(gross_salary - total_deductions - tax_info["total_tax"]),
        "net_monthly": round(net_monthly),
        "regime": regime,
    }


def salary_breakup(
    ctc: float,
    metro: bool = True,
    epf_on_full: bool = False,
) -> dict:
    """CTC to in-hand — Labour Code 2025 compliant (Basic ≥ 50% of gross wages).

    Args:
        ctc: Annual CTC.
        metro: True for Delhi/Mumbai/Kolkata/Chennai (50% HRA) else 40%.
        epf_on_full: If True, PF on full basic (not capped at ₹15K).

    Returns:
        Dict with full breakup including ESI applicability.
    """
    basic_monthly = round(ctc * 0.50 / 12)
    hra_monthly = round(basic_monthly * (0.50 if metro else 0.40))
    epf_base = basic_monthly if epf_on_full else min(basic_monthly, 15000)
    employee_pf = round(epf_base * 0.12 * 12)
    employer_pf = round(epf_base * 0.12 * 12)
    employer_pension = round(min(epf_base, 15000) * 0.0833 * 12)
    gratuity_annual = round(basic_monthly * 15 / 26)
    gross_monthly = round(ctc / 12)
    esi_applicable = gross_monthly <= 21000
    esi_employee = round(gross_monthly * 0.0075 * 12) if esi_applicable else 0
    esi_employer = round(gross_monthly * 0.0325 * 12) if esi_applicable else 0
    special_allowance = ctc - basic_monthly * 12 - hra_monthly * 12 - employer_pf - employer_pension - gratuity_annual - esi_employer
    in_hand_annual = basic_monthly * 12 + hra_monthly * 12 + max(special_allowance, 0) - employee_pf - esi_employee

    return {
        "basic_annual": basic_monthly * 12,
        "basic_monthly": basic_monthly,
        "hra_annual": hra_monthly * 12,
        "hra_monthly": hra_monthly,
        "special_allowance": round(max(special_allowance, 0)),
        "employee_pf": employee_pf,
        "employer_pf": employer_pf,
        "employer_pension": employer_pension,
        "gratuity_provision": gratuity_annual,
        "esi_employee": esi_employee,
        "esi_employer": esi_employer,
        "esi_applicable": esi_applicable,
        "gross_annual": ctc,
        "in_hand_annual": round(in_hand_annual),
        "in_hand_monthly": round(in_hand_annual / 12),
        "note": "Labour Code compliant (Basic >= 50% of gross wages)",
    }


def esi_contribution(gross_monthly: float) -> dict:
    """ESI contribution calculator.

    ESI applicable if gross monthly salary ≤ ₹21,000.
    Employee: 0.75%, Employer: 3.25%.

    Args:
        gross_monthly: Monthly gross salary.

    Returns:
        Dict with applicability and contribution amounts.
    """
    if gross_monthly > 21000:
        return {"applicable": False, "employee": 0, "employer": 0, "total": 0}
    employee = round(gross_monthly * 0.0075)
    employer = round(gross_monthly * 0.0325)
    return {
        "applicable": True,
        "employee": employee,
        "employer": employer,
        "total": employee + employer,
        "annual_employee": employee * 12,
        "annual_employer": employer * 12,
    }
