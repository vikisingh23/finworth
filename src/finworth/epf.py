"""Employee Provident Fund calculator — maturity with employer match."""

from __future__ import annotations


def epf_maturity(
    basic_da: float,
    rate: float = 0.081,
    years: int = 30,
    employee_percent: float = 0.12,
    employer_percent: float = 0.0367,
    annual_increment: float = 0.05,
) -> dict:
    """EPF corpus projection.

    Args:
        basic_da: Current monthly Basic + DA.
        rate: EPF interest rate as decimal (8.1% for FY 2024-25).
        years: Years until retirement.
        employee_percent: Employee contribution (12% of basic).
        employer_percent: Employer PF contribution (3.67% of basic, rest goes to EPS).
        annual_increment: Expected annual salary increment.

    Returns:
        Dict with total corpus, employee share, employer share, interest earned.

    Example:
        >>> epf_maturity(50000, 0.081, 30)
    """
    balance = 0
    total_employee = 0
    total_employer = 0
    current_basic = basic_da

    for year in range(1, years + 1):
        monthly_employee = min(current_basic, 15000) * employee_percent
        monthly_employer = min(current_basic, 15000) * employer_percent
        yearly_employee = monthly_employee * 12
        yearly_employer = monthly_employer * 12

        balance += yearly_employee + yearly_employer
        interest = balance * rate
        balance += interest

        total_employee += yearly_employee
        total_employer += yearly_employer
        current_basic *= (1 + annual_increment)

    return {
        "total_corpus": round(balance),
        "employee_contribution": round(total_employee),
        "employer_contribution": round(total_employer),
        "total_contributed": round(total_employee + total_employer),
        "interest_earned": round(balance - total_employee - total_employer),
        "rate": rate,
        "years": years,
    }
