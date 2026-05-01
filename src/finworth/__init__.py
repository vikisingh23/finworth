"""finworth — Indian financial calculators for MF, Stocks, FD, RD, PPF, NPS."""

__version__ = "0.2.0"

from finworth.core import xirr, cagr, absolute_return, inflation_adjusted
from finworth.mf import sip_maturity, swp_projection, mf_capital_gains, sip_xirr
from finworth.fd import fd_maturity, fd_post_tax, fd_compare
from finworth.rd import rd_maturity, rd_effective_yield
from finworth.ppf import ppf_maturity, ppf_extension
from finworth.nps import nps_maturity, nps_tax_benefit
from finworth.stocks import stock_pnl, dividend_yield, delivery_charges, intraday_charges
from finworth.tax import stt, gst_on_brokerage, stamp_duty, tds_on_fd, tds_on_rd, income_tax_slab, income_tax_compare

__all__ = [
    "xirr", "cagr", "absolute_return", "inflation_adjusted",
    "sip_maturity", "swp_projection", "mf_capital_gains", "sip_xirr",
    "fd_maturity", "fd_post_tax", "fd_compare",
    "rd_maturity", "rd_effective_yield",
    "ppf_maturity", "ppf_extension",
    "nps_maturity", "nps_tax_benefit",
    "stock_pnl", "dividend_yield", "delivery_charges", "intraday_charges",
    "stt", "gst_on_brokerage", "stamp_duty", "tds_on_fd", "tds_on_rd",
    "income_tax_slab", "income_tax_compare",
]
