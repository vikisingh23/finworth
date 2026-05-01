"""Indian tax calculators — STT, GST, stamp duty, TDS, income tax slabs (FY 2019-20 to 2024-25)."""

from __future__ import annotations
from typing import Literal

# All tax slabs from FY 2019-20 onwards
TAX_SLABS = {
    # OLD REGIME (unchanged since 2019)
    "old": {
        "2019-20": {"slabs": [(250000, 0), (250000, 0.05), (500000, 0.20), (float("inf"), 0.30)], "std_deduction": 50000, "rebate_limit": 500000},
        "2020-21": {"slabs": [(250000, 0), (250000, 0.05), (500000, 0.20), (float("inf"), 0.30)], "std_deduction": 50000, "rebate_limit": 500000},
        "2021-22": {"slabs": [(250000, 0), (250000, 0.05), (500000, 0.20), (float("inf"), 0.30)], "std_deduction": 50000, "rebate_limit": 500000},
        "2022-23": {"slabs": [(250000, 0), (250000, 0.05), (500000, 0.20), (float("inf"), 0.30)], "std_deduction": 50000, "rebate_limit": 500000},
        "2023-24": {"slabs": [(250000, 0), (250000, 0.05), (500000, 0.20), (float("inf"), 0.30)], "std_deduction": 50000, "rebate_limit": 500000},
        "2024-25": {"slabs": [(250000, 0), (250000, 0.05), (500000, 0.20), (float("inf"), 0.30)], "std_deduction": 50000, "rebate_limit": 500000},
    },
    # NEW REGIME
    "new": {
        # FY 2020-21 to 2022-23 (Budget 2020 — optional, no deductions)
        "2020-21": {"slabs": [(250000, 0), (250000, 0.05), (250000, 0.10), (250000, 0.15), (250000, 0.20), (250000, 0.25), (float("inf"), 0.30)], "std_deduction": 0, "rebate_limit": 500000},
        "2021-22": {"slabs": [(250000, 0), (250000, 0.05), (250000, 0.10), (250000, 0.15), (250000, 0.20), (250000, 0.25), (float("inf"), 0.30)], "std_deduction": 0, "rebate_limit": 500000},
        "2022-23": {"slabs": [(250000, 0), (250000, 0.05), (250000, 0.10), (250000, 0.15), (250000, 0.20), (250000, 0.25), (float("inf"), 0.30)], "std_deduction": 0, "rebate_limit": 500000},
        # FY 2023-24 (Budget 2023 — default regime, revised slabs)
        "2023-24": {"slabs": [(300000, 0), (300000, 0.05), (300000, 0.10), (300000, 0.15), (300000, 0.20), (float("inf"), 0.30)], "std_deduction": 50000, "rebate_limit": 700000},
        # FY 2024-25 (Budget 2024 — revised slabs + higher std deduction)
        "2024-25": {"slabs": [(300000, 0), (400000, 0.05), (300000, 0.10), (200000, 0.15), (300000, 0.20), (float("inf"), 0.30)], "std_deduction": 75000, "rebate_limit": 700000},
    },
}


def income_tax_slab(
    income: float,
    regime: Literal["old", "new"] = "new",
    fy: str = "2024-25",
) -> dict:
    """Indian income tax calculation with historical slab support.

    Args:
        income: Total taxable income (gross salary for salaried).
        regime: 'old' or 'new' tax regime.
        fy: Financial year — '2019-20' to '2024-25'.

    Returns:
        Dict with taxable_income, slab_wise breakdown, tax, cess, total_tax, effective_rate.

    Example:
        >>> income_tax_slab(1500000, "new", "2024-25")
        >>> income_tax_slab(1200000, "old", "2022-23")
    """
    if regime == "new" and fy == "2019-20":
        # New regime didn't exist in 2019-20, fall back to old
        regime = "old"

    config = TAX_SLABS.get(regime, {}).get(fy)
    if not config:
        raise ValueError(f"No slab data for regime='{regime}', fy='{fy}'. Supported: 2019-20 to 2024-25")

    slabs = config["slabs"]
    std_deduction = config["std_deduction"]
    rebate_limit = config["rebate_limit"]

    taxable = max(income - std_deduction, 0)
    tax = 0
    remaining = taxable
    slab_breakdown = []

    for slab_limit, rate in slabs:
        if remaining <= 0:
            break
        taxable_in_slab = min(remaining, slab_limit)
        tax_in_slab = taxable_in_slab * rate
        tax += tax_in_slab
        remaining -= taxable_in_slab
        if taxable_in_slab > 0:
            slab_breakdown.append({
                "slab": f"{rate*100:.0f}%",
                "amount": round(taxable_in_slab),
                "tax": round(tax_in_slab),
            })

    # Section 87A rebate
    if taxable <= rebate_limit:
        rebate = min(tax, 12500) if fy in ("2019-20", "2020-21", "2021-22", "2022-23") else min(tax, 25000)
        tax = max(tax - rebate, 0)

    surcharge = _calculate_surcharge(tax, taxable, fy)
    cess = (tax + surcharge) * 0.04
    total = tax + surcharge + cess

    return {
        "fy": fy,
        "regime": regime,
        "gross_income": round(income),
        "standard_deduction": round(std_deduction),
        "taxable_income": round(taxable),
        "slab_breakdown": slab_breakdown,
        "tax_before_cess": round(tax),
        "surcharge": round(surcharge),
        "cess": round(cess),
        "total_tax": round(total),
        "effective_rate": round(total / income, 6) if income > 0 else 0,
    }


def _calculate_surcharge(tax: float, taxable_income: float, fy: str) -> float:
    """Surcharge on income tax."""
    if taxable_income <= 5000000:
        return 0
    elif taxable_income <= 10000000:
        return tax * 0.10
    elif taxable_income <= 20000000:
        return tax * 0.15
    elif taxable_income <= 50000000:
        return tax * 0.25
    else:
        return tax * 0.37


def income_tax_compare(income: float, fy: str = "2024-25") -> dict:
    """Compare old vs new regime for a given income and FY.

    Returns:
        Dict with old_regime, new_regime, and recommendation.
    """
    old = income_tax_slab(income, "old", fy)
    new = income_tax_slab(income, "new", fy)
    savings = old["total_tax"] - new["total_tax"]

    return {
        "old_regime": old,
        "new_regime": new,
        "savings_with_new": round(savings),
        "recommendation": "new" if savings >= 0 else "old",
    }


def stt(value: float, trade_type: Literal["equity_delivery", "equity_intraday", "futures", "options"] = "equity_delivery") -> float:
    """Securities Transaction Tax."""
    rates = {
        "equity_delivery": 0.001,
        "equity_intraday": 0.00025,
        "futures": 0.0125 / 100,
        "options": 0.0625 / 100,
    }
    return round(value * rates.get(trade_type, 0), 2)


def gst_on_brokerage(brokerage: float, exchange_charges: float = 0) -> float:
    """GST on brokerage + exchange charges (18%)."""
    return round((brokerage + exchange_charges) * 0.18, 2)


def stamp_duty(value: float, instrument: Literal["equity_delivery", "equity_intraday", "futures", "options", "mf"] = "equity_delivery") -> float:
    """Stamp duty on buy-side transactions."""
    rates = {
        "equity_delivery": 0.00015,
        "equity_intraday": 0.00003,
        "futures": 0.00002,
        "options": 0.00003,
        "mf": 0.00005,
    }
    return round(value * rates.get(instrument, 0), 2)


def tds_on_fd(interest: float, is_senior_citizen: bool = False) -> dict:
    """TDS on Fixed Deposit interest (Section 194A)."""
    limit = 50000 if is_senior_citizen else 40000
    if interest <= limit:
        return {"tds_applicable": False, "tds_amount": 0, "net_interest": round(interest, 2)}
    tds = round(interest * 0.10, 2)
    return {"tds_applicable": True, "tds_amount": tds, "net_interest": round(interest - tds, 2)}


def tds_on_rd(interest: float, is_senior_citizen: bool = False) -> dict:
    """TDS on Recurring Deposit interest."""
    return tds_on_fd(interest, is_senior_citizen)
