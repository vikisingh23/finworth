"""Mutual Fund calculators — SIP, SWP, capital gains."""

from __future__ import annotations
from datetime import date
from typing import Literal


def sip_maturity(monthly: float, rate: float, years: int) -> dict:
    """SIP future value calculator.

    Args:
        monthly: Monthly SIP amount.
        rate: Expected annual return as decimal (0.12 = 12%).
        years: Investment duration in years.

    Returns:
        Dict with invested, returns, maturity, and effective_cagr.

    Example:
        >>> sip_maturity(10000, 0.12, 10)
        {'invested': 1200000, 'returns': 1123391, 'maturity': 2323391, 'effective_cagr': 0.120}
    """
    n = years * 12
    r = rate / 12
    if r == 0:
        fv = monthly * n
    else:
        fv = monthly * (((1 + r) ** n - 1) / r) * (1 + r)
    invested = monthly * n
    returns = fv - invested
    return {
        "invested": round(invested),
        "returns": round(returns),
        "maturity": round(fv),
    }


def sip_xirr(monthly: float, current_value: float, months: int) -> float:
    """Approximate XIRR for a running SIP.

    Args:
        monthly: Monthly SIP amount.
        current_value: Current portfolio value.
        months: Number of months invested.

    Returns:
        Annualized return as decimal.
    """
    from finworth.core import xirr as _xirr
    from datetime import timedelta

    start = date(2020, 1, 1)
    cashflows = [(start + timedelta(days=30 * i), -monthly) for i in range(months)]
    cashflows.append((start + timedelta(days=30 * months), current_value))
    return _xirr(cashflows)


def swp_projection(corpus: float, monthly_withdrawal: float, rate: float, years: int) -> dict:
    """Systematic Withdrawal Plan projection.

    Args:
        corpus: Initial investment amount.
        monthly_withdrawal: Monthly withdrawal amount.
        rate: Expected annual return as decimal.
        years: Projection period.

    Returns:
        Dict with total_withdrawn, remaining_corpus, and months_sustainable.

    Example:
        >>> swp_projection(5000000, 30000, 0.08, 10)
    """
    r = rate / 12
    balance = corpus
    total_withdrawn = 0
    months_sustained = 0

    for m in range(years * 12):
        balance *= (1 + r)
        if balance < monthly_withdrawal:
            total_withdrawn += balance
            months_sustained = m + 1
            balance = 0
            break
        balance -= monthly_withdrawal
        total_withdrawn += monthly_withdrawal
        months_sustained = m + 1

    return {
        "total_withdrawn": round(total_withdrawn),
        "remaining_corpus": round(balance),
        "months_sustainable": months_sustained,
        "corpus_exhausted": balance <= 0,
    }


def mf_capital_gains(
    buy_nav: float,
    sell_nav: float,
    units: float,
    holding_days: int,
    fund_type: Literal["equity", "debt"] = "equity",
    cost_inflation_index_buy: int | None = None,
    cost_inflation_index_sell: int | None = None,
) -> dict:
    """Mutual fund capital gains calculation (Indian tax rules FY 2024-25+).

    Args:
        buy_nav: Purchase NAV.
        sell_nav: Redemption NAV.
        units: Number of units.
        holding_days: Days between buy and sell.
        fund_type: 'equity' or 'debt'.
        cost_inflation_index_buy: CII for buy year (debt LTCG before Apr 2023).
        cost_inflation_index_sell: CII for sell year.

    Returns:
        Dict with gain, gain_type, tax_rate, and tax_amount.
    """
    buy_value = buy_nav * units
    sell_value = sell_nav * units
    gain = sell_value - buy_value

    if fund_type == "equity":
        if holding_days > 365:
            gain_type = "LTCG"
            exempt = min(max(gain, 0), 125000)  # ₹1.25L exemption (FY 2024-25+)
            taxable = max(gain - exempt, 0)
            tax_rate = 0.125  # 12.5% LTCG
        else:
            gain_type = "STCG"
            taxable = max(gain, 0)
            tax_rate = 0.20  # 20% STCG
    else:  # debt
        # Post Apr 2023: no indexation, taxed at slab rate
        if holding_days > 365 * 2:
            gain_type = "LTCG"
        else:
            gain_type = "STCG"
        taxable = max(gain, 0)
        tax_rate = None  # slab rate — caller should apply income_tax_slab()

    tax_amount = round(taxable * tax_rate, 2) if tax_rate else None

    return {
        "buy_value": round(buy_value, 2),
        "sell_value": round(sell_value, 2),
        "gain": round(gain, 2),
        "gain_type": gain_type,
        "taxable_gain": round(taxable, 2),
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
    }
