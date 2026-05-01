"""Pre-built workflows that chain multiple finworth calculators.

Usage:
    from finworth.workflows import financial_health_check, investment_compare
"""

from __future__ import annotations
from finworth.salary import hra_exemption, ctc_to_inhand
from finworth.tax import income_tax_slab, income_tax_compare
from finworth.epf import epf_maturity
from finworth.nps import nps_maturity, nps_tax_benefit
from finworth.ppf import ppf_maturity
from finworth.mf import sip_maturity
from finworth.fd import fd_maturity, fd_post_tax
from finworth.rd import rd_maturity
from finworth.gratuity import gratuity
from finworth.planning import retirement_corpus, future_cost
from finworth.emi import emi


def financial_health_check(
    ctc: float,
    age: int,
    monthly_rent: float = 0,
    metro: bool = True,
    monthly_expense: float | None = None,
    retirement_age: int = 60,
    existing_corpus: float = 0,
    home_loan_principal: float = 0,
    home_loan_rate: float = 0.085,
    home_loan_years: int = 20,
    nps_monthly: float = 0,
) -> dict:
    """Complete financial health check from a single set of inputs.

    Args:
        ctc: Annual CTC.
        age: Current age.
        monthly_rent: Monthly rent (0 if own house).
        metro: Metro city for HRA calculation.
        monthly_expense: Monthly expense (estimated as 60% of in-hand if not provided).
        retirement_age: Target retirement age.
        existing_corpus: Current savings/investments.
        home_loan_principal: Outstanding home loan (0 if none).
        home_loan_rate: Home loan interest rate.
        home_loan_years: Remaining home loan tenure.
        nps_monthly: Monthly NPS contribution (0 if none).

    Returns:
        Comprehensive financial snapshot with actionable insights.
    """
    # 1. Salary breakup
    salary_new = ctc_to_inhand(ctc, regime="new")
    salary_old = ctc_to_inhand(ctc, regime="old")
    basic_monthly = ctc * 0.40 / 12
    hra_monthly = ctc * 0.20 / 12

    # 2. Tax comparison
    tax_compare = income_tax_compare(salary_new["gross_salary_annual"])

    # 3. HRA benefit (old regime only)
    hra = None
    if monthly_rent > 0:
        hra = hra_exemption(basic_monthly, hra_monthly, monthly_rent, metro)

    # 4. EPF projection
    years_to_retire = retirement_age - age
    epf = epf_maturity(basic_monthly, years=years_to_retire)

    # 5. NPS projection
    nps = None
    nps_tax = None
    if nps_monthly > 0:
        nps = nps_maturity(nps_monthly, years=years_to_retire)
        nps_tax = nps_tax_benefit(nps_monthly * 12, regime=tax_compare["recommendation"])

    # 6. Gratuity estimate
    grat = gratuity(basic_monthly, years_to_retire)

    # 7. Home loan
    loan = None
    if home_loan_principal > 0:
        loan = emi(home_loan_principal, home_loan_rate, home_loan_years)

    # 8. Retirement readiness
    net_monthly = salary_new["net_monthly"]
    if monthly_expense is None:
        monthly_expense = round(net_monthly * 0.60)

    retirement = retirement_corpus(monthly_expense, age, retirement_age)
    projected_corpus = existing_corpus + epf["total_corpus"] + grat["gratuity_amount"]
    if nps:
        projected_corpus += nps["lumpsum_withdrawal"]

    gap = retirement["corpus_needed"] - projected_corpus
    on_track = gap <= 0

    # 9. Monthly savings capacity
    monthly_obligations = (loan["emi"] if loan else 0) + (nps_monthly)
    monthly_savings_capacity = net_monthly - monthly_expense - monthly_obligations

    return {
        "salary": {
            "ctc": ctc,
            "monthly_inhand_new_regime": salary_new["net_monthly"],
            "monthly_inhand_old_regime": salary_old["net_monthly"],
            "recommended_regime": tax_compare["recommendation"],
            "tax_saved_with_recommendation": tax_compare["savings_with_new"],
        },
        "hra": hra,
        "epf_at_retirement": epf["total_corpus"],
        "nps_at_retirement": nps,
        "gratuity_at_retirement": grat["gratuity_amount"],
        "home_loan": loan,
        "retirement": {
            "monthly_expense_today": monthly_expense,
            "expense_at_retirement": retirement["expense_at_retirement"],
            "corpus_needed": retirement["corpus_needed"],
            "projected_corpus": round(projected_corpus),
            "gap": round(max(gap, 0)),
            "on_track": on_track,
            "additional_sip_needed": round(gap / (((1 + 0.01) ** (years_to_retire * 12) - 1) / 0.01)) if gap > 0 else 0,
        },
        "monthly_budget": {
            "inhand": net_monthly,
            "expense": monthly_expense,
            "emi": loan["emi"] if loan else 0,
            "nps": nps_monthly,
            "available_to_invest": round(monthly_savings_capacity),
        },
    }


def investment_compare(
    monthly: float,
    years: int,
    tax_slab: float = 0.3,
    lumpsum: float = 0,
) -> dict:
    """Compare the same amount across all investment options.

    Args:
        monthly: Monthly investment amount.
        years: Investment horizon.
        tax_slab: Income tax slab for post-tax calculations.
        lumpsum: One-time investment (in addition to monthly).

    Returns:
        Side-by-side comparison sorted by post-tax returns.
    """
    invested = monthly * 12 * years + lumpsum

    # SIP in equity MF (12% pre-tax)
    mf_equity = sip_maturity(monthly, 0.12, years)
    mf_equity_tax = mf_equity["returns"] * 0.125 * 0.5  # rough: 12.5% LTCG on ~50% gains above 1.25L
    mf_equity_post = mf_equity["maturity"] - mf_equity_tax

    # SIP in debt MF (7% pre-tax)
    mf_debt = sip_maturity(monthly, 0.07, years)
    mf_debt_tax = mf_debt["returns"] * tax_slab
    mf_debt_post = mf_debt["maturity"] - mf_debt_tax

    # FD (7% quarterly compounding)
    fd = fd_post_tax(invested, 0.07, years, tax_slab)

    # RD (6.5%)
    rd = rd_maturity(monthly, 0.065, years)
    rd_tax = rd["interest_earned"] * tax_slab
    rd_post = rd["maturity"] - rd_tax

    # PPF (7.1%, tax-free)
    ppf_yearly = min(monthly * 12, 150000)
    ppf = ppf_maturity(ppf_yearly, 0.071, min(years, 15))

    # NPS (10%, partial tax on withdrawal)
    nps = nps_maturity(monthly, 0.10, years)
    nps_post = nps["lumpsum_withdrawal"] + (nps["annuity_corpus"] * 0.60)  # 60% of annuity taxable

    # EPF (8.1%, tax-free up to 2.5L/yr contribution)
    epf = epf_maturity(monthly / 0.12, 0.081, years)  # reverse-engineer basic from 12% contribution

    options = [
        {"name": "Equity MF (SIP)", "pre_tax": mf_equity["maturity"], "post_tax": round(mf_equity_post), "tax_free": False, "risk": "High", "lock_in": "None"},
        {"name": "Debt MF (SIP)", "pre_tax": mf_debt["maturity"], "post_tax": round(mf_debt_post), "tax_free": False, "risk": "Low", "lock_in": "None"},
        {"name": "FD", "pre_tax": fd["pre_tax_maturity"], "post_tax": fd["post_tax_maturity"], "tax_free": False, "risk": "None", "lock_in": "Flexible"},
        {"name": "RD", "pre_tax": rd["maturity"], "post_tax": round(rd_post), "tax_free": False, "risk": "None", "lock_in": "Fixed"},
        {"name": "PPF", "pre_tax": ppf["maturity"], "post_tax": ppf["maturity"], "tax_free": True, "risk": "None", "lock_in": "15 years"},
        {"name": "NPS", "pre_tax": nps["total_corpus"], "post_tax": round(nps_post), "tax_free": False, "risk": "Medium", "lock_in": "Till 60"},
        {"name": "EPF", "pre_tax": epf["total_corpus"], "post_tax": epf["total_corpus"], "tax_free": True, "risk": "None", "lock_in": "Till retirement"},
    ]

    for opt in options:
        opt["invested"] = round(invested) if opt["name"] != "EPF" else epf["total_contributed"]
        opt["absolute_return"] = round((opt["post_tax"] - opt["invested"]) / opt["invested"] * 100, 1) if opt["invested"] > 0 else 0

    options.sort(key=lambda x: x["post_tax"], reverse=True)

    return {
        "monthly_investment": monthly,
        "years": years,
        "tax_slab": tax_slab,
        "comparison": options,
        "best_option": options[0]["name"],
        "best_post_tax_value": options[0]["post_tax"],
    }
