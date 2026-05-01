"""National Pension System calculator — corpus, annuity, tax benefits."""

from __future__ import annotations
from typing import Literal


def nps_maturity(
    monthly: float,
    rate: float = 0.10,
    years: int = 30,
    annuity_percent: float = 0.40,
    annuity_rate: float = 0.06,
) -> dict:
    """NPS corpus and pension projection.

    Args:
        monthly: Monthly contribution.
        rate: Expected annual return as decimal (equity ~10%, corporate bond ~8%, govt ~7%).
        years: Years until retirement.
        annuity_percent: Percentage of corpus for annuity (min 40%).
        annuity_rate: Annuity provider's annual rate.

    Returns:
        Dict with total corpus, lumpsum, annuity corpus, and monthly pension.

    Example:
        >>> nps_maturity(5000, 0.10, 30)
    """
    annuity_percent = max(annuity_percent, 0.40)  # min 40% annuity mandatory
    n = years * 12
    r = rate / 12

    if r == 0:
        corpus = monthly * n
    else:
        corpus = monthly * (((1 + r) ** n - 1) / r) * (1 + r)

    invested = monthly * n
    annuity_corpus = corpus * annuity_percent
    lumpsum = corpus * (1 - annuity_percent)
    monthly_pension = (annuity_corpus * annuity_rate) / 12

    return {
        "invested": round(invested),
        "total_corpus": round(corpus),
        "wealth_gain": round(corpus - invested),
        "lumpsum_withdrawal": round(lumpsum),
        "annuity_corpus": round(annuity_corpus),
        "monthly_pension": round(monthly_pension),
        "annuity_percent": annuity_percent,
    }


def nps_tax_benefit(
    contribution: float,
    employer_contribution: float = 0,
    regime: Literal["old", "new"] = "new",
    tax_slab: float = 0.3,
) -> dict:
    """NPS tax deduction benefits.

    Args:
        contribution: Annual self-contribution.
        employer_contribution: Annual employer contribution (for salaried).
        regime: Tax regime.
        tax_slab: Marginal tax slab rate.

    Returns:
        Dict with deductions under 80CCD(1), 80CCD(1B), 80CCD(2) and total tax saved.
    """
    # 80CCD(1) — employee contribution, part of 80C (₹1.5L limit)
    sec_80ccd1 = min(contribution, 150000)

    # 80CCD(1B) — additional ₹50K deduction (old regime only)
    sec_80ccd1b = min(max(contribution - sec_80ccd1, 0), 50000) if regime == "old" else 0

    # 80CCD(2) — employer contribution (max 10% of basic+DA for private, 14% for govt)
    sec_80ccd2 = employer_contribution  # no upper limit in new regime

    total_deduction = sec_80ccd1 + sec_80ccd1b + sec_80ccd2
    tax_saved = round(total_deduction * tax_slab)

    return {
        "sec_80ccd1": round(sec_80ccd1),
        "sec_80ccd1b": round(sec_80ccd1b),
        "sec_80ccd2": round(sec_80ccd2),
        "total_deduction": round(total_deduction),
        "tax_saved": tax_saved,
        "regime": regime,
    }
