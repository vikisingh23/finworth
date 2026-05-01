"""Indian tax calculators — STT, GST, stamp duty, TDS, income tax slabs."""

from __future__ import annotations
from typing import Literal


def stt(value: float, trade_type: Literal["equity_delivery", "equity_intraday", "futures", "options"] = "equity_delivery") -> float:
    """Securities Transaction Tax.

    Args:
        value: Transaction value (sell-side for delivery/intraday, premium for options).
        trade_type: Type of trade.

    Returns:
        STT amount.
    """
    rates = {
        "equity_delivery": 0.001,     # 0.1% on sell
        "equity_intraday": 0.00025,   # 0.025% on sell
        "futures": 0.0125 / 100,      # 0.0125% on sell
        "options": 0.0625 / 100,      # 0.0625% on premium (sell)
    }
    return round(value * rates.get(trade_type, 0), 2)


def gst_on_brokerage(brokerage: float, exchange_charges: float = 0) -> float:
    """GST on brokerage + exchange transaction charges (18%).

    Args:
        brokerage: Brokerage amount.
        exchange_charges: Exchange transaction charges.

    Returns:
        GST amount.
    """
    return round((brokerage + exchange_charges) * 0.18, 2)


def stamp_duty(value: float, instrument: Literal["equity_delivery", "equity_intraday", "futures", "options", "mf"] = "equity_delivery") -> float:
    """Stamp duty on buy-side transactions.

    Args:
        value: Buy-side transaction value.
        instrument: Type of instrument.

    Returns:
        Stamp duty amount.
    """
    rates = {
        "equity_delivery": 0.00015,   # 0.015%
        "equity_intraday": 0.00003,   # 0.003%
        "futures": 0.00002,           # 0.002%
        "options": 0.00003,           # 0.003%
        "mf": 0.00005,               # 0.005%
    }
    return round(value * rates.get(instrument, 0), 2)


def tds_on_fd(interest: float, is_senior_citizen: bool = False) -> dict:
    """TDS on Fixed Deposit interest (Section 194A).

    Args:
        interest: Annual interest earned.
        is_senior_citizen: Senior citizens get ₹50K limit (vs ₹40K).

    Returns:
        Dict with tds_applicable, tds_amount, and net_interest.
    """
    limit = 50000 if is_senior_citizen else 40000
    if interest <= limit:
        return {"tds_applicable": False, "tds_amount": 0, "net_interest": round(interest, 2)}

    tds = round(interest * 0.10, 2)  # 10% TDS
    return {
        "tds_applicable": True,
        "tds_amount": tds,
        "net_interest": round(interest - tds, 2),
    }


def tds_on_rd(interest: float, is_senior_citizen: bool = False) -> dict:
    """TDS on Recurring Deposit interest (same rules as FD)."""
    return tds_on_fd(interest, is_senior_citizen)


def income_tax_slab(
    income: float,
    regime: Literal["old", "new"] = "new",
    fy: str = "2024-25",
) -> dict:
    """Indian income tax calculation.

    Args:
        income: Total taxable income.
        regime: 'old' or 'new' tax regime.
        fy: Financial year (currently supports 2024-25).

    Returns:
        Dict with tax, cess, total_tax, effective_rate.

    Example:
        >>> income_tax_slab(1500000, "new")
    """
    if regime == "new":
        # New regime FY 2024-25 (Budget 2024)
        slabs = [
            (300000, 0),
            (400000, 0.05),   # 3L - 7L: 5%
            (300000, 0.10),   # 7L - 10L: 10%
            (200000, 0.15),   # 10L - 12L: 15%
            (300000, 0.20),   # 12L - 15L: 20%
            (float("inf"), 0.30),  # 15L+: 30%
        ]
        standard_deduction = 75000
    else:
        # Old regime
        slabs = [
            (250000, 0),
            (250000, 0.05),   # 2.5L - 5L: 5%
            (500000, 0.20),   # 5L - 10L: 20%
            (float("inf"), 0.30),  # 10L+: 30%
        ]
        standard_deduction = 50000

    taxable = max(income - standard_deduction, 0)
    tax = 0
    remaining = taxable

    for slab_limit, rate in slabs:
        if remaining <= 0:
            break
        taxable_in_slab = min(remaining, slab_limit)
        tax += taxable_in_slab * rate
        remaining -= taxable_in_slab

    # Section 87A rebate (new regime: income up to ₹7L)
    if regime == "new" and taxable <= 700000:
        tax = 0

    cess = tax * 0.04  # 4% health & education cess
    total = tax + cess

    return {
        "taxable_income": round(taxable),
        "tax_before_cess": round(tax),
        "cess": round(cess),
        "total_tax": round(total),
        "effective_rate": round(total / income, 6) if income > 0 else 0,
    }
