"""Core financial calculations — XIRR, CAGR, absolute return, inflation adjustment."""

from __future__ import annotations
from datetime import date, datetime
from typing import Sequence


def xirr(cashflows: Sequence[tuple[date, float]], guess: float = 0.1, max_iter: int = 1000, tol: float = 1e-6) -> float:
    """Calculate XIRR (Extended Internal Rate of Return).

    Args:
        cashflows: List of (date, amount) tuples. Negative = outflow, positive = inflow.
        guess: Initial guess for the rate.
        max_iter: Maximum Newton-Raphson iterations.
        tol: Convergence tolerance.

    Returns:
        Annualized return as a decimal (0.12 = 12%).

    Example:
        >>> from datetime import date
        >>> xirr([(date(2020,1,1), -10000), (date(2021,1,1), 11200)])
        0.12
    """
    if not cashflows or len(cashflows) < 2:
        return 0.0

    dates, amounts = zip(*cashflows)
    d0 = min(dates)
    years = [(d - d0).days / 365.25 for d in dates]

    rate = guess
    for _ in range(max_iter):
        npv = sum(a / (1 + rate) ** y for a, y in zip(amounts, years))
        dnpv = sum(-y * a / (1 + rate) ** (y + 1) for a, y in zip(amounts, years))
        if abs(dnpv) < 1e-12:
            break
        new_rate = rate - npv / dnpv
        if abs(new_rate - rate) < tol:
            return round(new_rate, 6)
        rate = new_rate

    return round(rate, 6)


def cagr(initial: float, final: float, years: float) -> float:
    """Compound Annual Growth Rate.

    Args:
        initial: Starting value.
        final: Ending value.
        years: Time period in years.

    Returns:
        CAGR as decimal (0.15 = 15%).

    Example:
        >>> cagr(100000, 200000, 5)
        0.148698
    """
    if initial <= 0 or years <= 0:
        return 0.0
    return round((final / initial) ** (1 / years) - 1, 6)


def absolute_return(invested: float, current: float) -> float:
    """Simple absolute return.

    Returns:
        Return as decimal (0.20 = 20%).

    Example:
        >>> absolute_return(100000, 120000)
        0.2
    """
    if invested <= 0:
        return 0.0
    return round((current - invested) / invested, 6)


def inflation_adjusted(nominal_return: float, inflation: float) -> float:
    """Real return adjusted for inflation (Fisher equation).

    Args:
        nominal_return: Nominal return as decimal.
        inflation: Inflation rate as decimal.

    Returns:
        Real return as decimal.

    Example:
        >>> inflation_adjusted(0.12, 0.06)
        0.056604
    """
    return round((1 + nominal_return) / (1 + inflation) - 1, 6)
