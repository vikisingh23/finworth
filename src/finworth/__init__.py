"""finworth — Indian financial calculators for MF, Stocks, FD, RD."""

__version__ = "0.1.0"

from finworth.core import xirr, cagr, absolute_return, inflation_adjusted
from finworth.mf import sip_maturity, swp_projection, mf_capital_gains, sip_xirr
from finworth.fd import fd_maturity, fd_post_tax, fd_compare
from finworth.rd import rd_maturity, rd_effective_yield
from finworth.stocks import stock_pnl, dividend_yield, delivery_charges, intraday_charges
from finworth.tax import stt, gst_on_brokerage, stamp_duty, tds_on_fd, tds_on_rd, income_tax_slab

__all__ = [
    "xirr", "cagr", "absolute_return", "inflation_adjusted",
    "sip_maturity", "swp_projection", "mf_capital_gains", "sip_xirr",
    "fd_maturity", "fd_post_tax", "fd_compare",
    "rd_maturity", "rd_effective_yield",
    "stock_pnl", "dividend_yield", "delivery_charges", "intraday_charges",
    "stt", "gst_on_brokerage", "stamp_duty", "tds_on_fd", "tds_on_rd", "income_tax_slab",
]
