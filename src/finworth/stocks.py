"""Stock market calculators — P&L with charges, dividend yield, brokerage."""

from __future__ import annotations
from typing import Literal


def stock_pnl(
    buy_price: float,
    sell_price: float,
    quantity: int,
    trade_type: Literal["delivery", "intraday"] = "delivery",
    brokerage_per_order: float = 20,
) -> dict:
    """Stock P&L with all Indian charges (STT, GST, stamp duty, exchange fees).

    Args:
        buy_price: Buy price per share.
        sell_price: Sell price per share.
        quantity: Number of shares.
        trade_type: 'delivery' or 'intraday'.
        brokerage_per_order: Flat brokerage per order (default ₹20 for discount brokers).

    Returns:
        Dict with gross_pnl, charges breakdown, net_pnl, and effective_return.

    Example:
        >>> stock_pnl(100, 120, 100, "delivery")
    """
    buy_value = buy_price * quantity
    sell_value = sell_price * quantity
    turnover = buy_value + sell_value
    gross_pnl = sell_value - buy_value

    charges = delivery_charges(buy_value, sell_value, brokerage_per_order) if trade_type == "delivery" \
        else intraday_charges(buy_value, sell_value, brokerage_per_order)

    net_pnl = gross_pnl - charges["total_charges"]
    effective_return = net_pnl / buy_value if buy_value > 0 else 0

    return {
        "buy_value": round(buy_value, 2),
        "sell_value": round(sell_value, 2),
        "gross_pnl": round(gross_pnl, 2),
        "net_pnl": round(net_pnl, 2),
        "effective_return": round(effective_return, 6),
        "charges": charges,
    }


def delivery_charges(buy_value: float, sell_value: float, brokerage_per_order: float = 20) -> dict:
    """Calculate all charges for delivery trades (CNC).

    Rates as per NSE/BSE FY 2024-25.
    """
    brokerage = brokerage_per_order * 2
    stt_charge = sell_value * 0.001  # 0.1% on sell side
    exchange_txn = (buy_value + sell_value) * 0.0000297  # NSE equity
    gst = (brokerage + exchange_txn) * 0.18
    sebi_fee = (buy_value + sell_value) * 0.000001  # ₹10 per crore
    stamp = buy_value * 0.00015  # 0.015% on buy side
    dp_charge = 15.93  # per scrip (₹13.5 + GST)

    total = brokerage + stt_charge + exchange_txn + gst + sebi_fee + stamp + dp_charge

    return {
        "brokerage": round(brokerage, 2),
        "stt": round(stt_charge, 2),
        "exchange_txn_charge": round(exchange_txn, 2),
        "gst": round(gst, 2),
        "sebi_fee": round(sebi_fee, 2),
        "stamp_duty": round(stamp, 2),
        "dp_charge": round(dp_charge, 2),
        "total_charges": round(total, 2),
    }


def intraday_charges(buy_value: float, sell_value: float, brokerage_per_order: float = 20) -> dict:
    """Calculate all charges for intraday trades (MIS).

    Rates as per NSE/BSE FY 2024-25.
    """
    brokerage = brokerage_per_order * 2
    stt_charge = sell_value * 0.00025  # 0.025% on sell side
    exchange_txn = (buy_value + sell_value) * 0.0000297
    gst = (brokerage + exchange_txn) * 0.18
    sebi_fee = (buy_value + sell_value) * 0.000001
    stamp = buy_value * 0.00003  # 0.003% on buy side

    total = brokerage + stt_charge + exchange_txn + gst + sebi_fee + stamp

    return {
        "brokerage": round(brokerage, 2),
        "stt": round(stt_charge, 2),
        "exchange_txn_charge": round(exchange_txn, 2),
        "gst": round(gst, 2),
        "sebi_fee": round(sebi_fee, 2),
        "stamp_duty": round(stamp, 2),
        "total_charges": round(total, 2),
    }


def dividend_yield(annual_dividend: float, current_price: float) -> float:
    """Dividend yield calculation.

    Args:
        annual_dividend: Total annual dividend per share.
        current_price: Current market price per share.

    Returns:
        Yield as decimal (0.02 = 2%).

    Example:
        >>> dividend_yield(10, 500)
        0.02
    """
    if current_price <= 0:
        return 0.0
    return round(annual_dividend / current_price, 6)
