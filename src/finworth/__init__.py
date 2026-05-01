"""finworth — Complete Indian financial calculator library."""

__version__ = "0.6.0"

from finworth.core import xirr, cagr, absolute_return, inflation_adjusted
from finworth.mf import sip_maturity, swp_projection, mf_capital_gains, sip_xirr
from finworth.fd import fd_maturity, fd_post_tax, fd_compare
from finworth.rd import rd_maturity, rd_effective_yield
from finworth.ppf import ppf_maturity, ppf_extension
from finworth.nps import nps_maturity, nps_tax_benefit
from finworth.epf import epf_maturity
from finworth.emi import emi, emi_amortization, emi_prepayment_impact
from finworth.gratuity import gratuity
from finworth.salary import hra_exemption, ctc_to_inhand
from finworth.planning import ssy_maturity, lumpsum_maturity, future_cost, retirement_corpus
from finworth.stocks import stock_pnl, dividend_yield, delivery_charges, intraday_charges
from finworth.tax import stt, gst_on_brokerage, stamp_duty, tds_on_fd, tds_on_rd, income_tax_slab, income_tax_compare
from finworth.workflows import financial_health_check, investment_compare

__all__ = [
    "xirr", "cagr", "absolute_return", "inflation_adjusted",
    "sip_maturity", "swp_projection", "mf_capital_gains", "sip_xirr",
    "fd_maturity", "fd_post_tax", "fd_compare",
    "rd_maturity", "rd_effective_yield",
    "ppf_maturity", "ppf_extension",
    "nps_maturity", "nps_tax_benefit",
    "epf_maturity",
    "emi", "emi_amortization", "emi_prepayment_impact",
    "gratuity",
    "hra_exemption", "ctc_to_inhand",
    "ssy_maturity", "lumpsum_maturity", "future_cost", "retirement_corpus",
    "stock_pnl", "dividend_yield", "delivery_charges", "intraday_charges",
    "stt", "gst_on_brokerage", "stamp_duty", "tds_on_fd", "tds_on_rd",
    "income_tax_slab", "income_tax_compare",
]
