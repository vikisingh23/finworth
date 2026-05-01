# finworth

Complete Indian financial calculator library. MF, Stocks, FD, RD, PPF, NPS, EPF, EMI, Gratuity, Tax, Salary, Retirement — with AI agent integration.

```
pip install finworth
```

Zero dependencies. Pure Python. 85 tests. Works everywhere.

Also available as an **MCP server** for AI agents (Claude, Kiro, Cursor).

---

## What's Inside

| Module | Calculators |
|--------|------------|
| **Core** | XIRR, CAGR, absolute return, inflation-adjusted return |
| **Mutual Funds** | SIP maturity, SIP XIRR, SWP projection, capital gains (LTCG/STCG) |
| **Fixed Deposits** | Maturity, post-tax returns, bank comparison |
| **Recurring Deposits** | Maturity, effective yield |
| **PPF** | 15-year maturity, extension blocks |
| **NPS** | Corpus projection, monthly pension, tax benefits (80CCD) |
| **EPF** | Corpus with employer match and annual increments |
| **EMI** | Monthly EMI, amortization schedule, prepayment impact |
| **Gratuity** | Payment of Gratuity Act (private + government) |
| **Salary** | HRA exemption (10(13A)), CTC to in-hand breakup |
| **Planning** | SSY, lumpsum, future cost (inflation), retirement corpus |
| **Stocks** | P&L with all charges (STT, GST, stamp duty, SEBI, DP) |
| **Tax** | Income tax slabs 2019-2025 (old + new regime), regime comparison, STT, TDS, surcharge |
| **Workflows** | One-call financial health check, investment comparison across 7 products |
| **AI** | MCP server, OpenAI function schemas, natural language tool discovery |

All calculations follow **Indian tax rules (FY 2024-25)** — SEBI, NSE/BSE charges, Income Tax Act, Payment of Gratuity Act.

---

## Quick Start

```python
import finworth as fw
from datetime import date

# XIRR
fw.xirr([(date(2021,1,1), -100000), (date(2024,1,1), 145000)])  # → 0.1318

# SIP
fw.sip_maturity(10000, 0.12, 10)  # → ₹23.2L from ₹12L invested

# FD post-tax
fw.fd_post_tax(500000, 0.07, 3, tax_slab=0.3)  # → 5.13% post-tax rate

# EMI
fw.emi(5000000, 0.085, 20)  # → ₹43,391/month

# Income tax
fw.income_tax_slab(1500000, "new")  # → ₹1.3L tax, 8.67% effective

# Old vs new regime
fw.income_tax_compare(1500000)  # → recommends best regime

# Stock P&L with all charges
fw.stock_pnl(500, 580, 200, "delivery")  # → ₹15,798 net after charges

# CTC to in-hand
fw.ctc_to_inhand(1500000)  # → full salary breakup with monthly in-hand

# Retirement planning
fw.retirement_corpus(50000, current_age=30)  # → corpus needed + SIP required
```

---

## Workflows

### Financial Health Check — one call, full picture

```python
health = fw.financial_health_check(
    ctc=1500000, age=30, monthly_rent=25000, nps_monthly=5000
)
health["salary"]["recommended_regime"]          # "new"
health["retirement"]["corpus_needed"]           # ₹3.2Cr
health["retirement"]["on_track"]                # False
health["monthly_budget"]["available_to_invest"] # ₹28,000
```

### Investment Comparison — same amount across 7 products

```python
compare = fw.investment_compare(monthly=10000, years=10)
for opt in compare["comparison"]:
    print(f"{opt['name']:20s} → ₹{opt['post_tax']:>12,}  ({opt['absolute_return']}%)")
```

---

## AI Agent Integration

### MCP Server (Claude, Kiro, Cursor)

Add to `.mcp.json`:
```json
{
  "finworth": {
    "command": "python3",
    "args": ["-m", "finworth.mcp_server"]
  }
}
```

Now any AI agent can call `sip_maturity`, `emi`, `income_tax_slab`, `financial_health_check` etc. as native tools.

### OpenAI Function Calling

```python
from finworth.ai import get_openai_functions
functions = get_openai_functions()  # pass to ChatCompletion API
```

### Natural Language → Function

```python
from finworth.ai import find_tool, execute
tool = find_tool("calculate my home loan EMI")
result = execute("emi", principal=5000000, rate=0.085, years=20)
```

---

## All Functions

<details>
<summary><strong>Core</strong></summary>

```python
fw.xirr(cashflows)                              # XIRR for irregular cashflows
fw.cagr(initial, final, years)                   # Compound annual growth rate
fw.absolute_return(invested, current)            # Simple return
fw.inflation_adjusted(nominal_return, inflation) # Real return
```
</details>

<details>
<summary><strong>Mutual Funds</strong></summary>

```python
fw.sip_maturity(monthly, rate, years)
fw.sip_xirr(monthly, current_value, months)
fw.swp_projection(corpus, monthly_withdrawal, rate, years)
fw.mf_capital_gains(buy_nav, sell_nav, units, holding_days, fund_type)
```
</details>

<details>
<summary><strong>FD & RD</strong></summary>

```python
fw.fd_maturity(principal, rate, years, compounding)
fw.fd_post_tax(principal, rate, years, tax_slab)
fw.fd_compare(principal, options, years)
fw.rd_maturity(monthly, rate, years)
fw.rd_effective_yield(rate)
```
</details>

<details>
<summary><strong>PPF, NPS, EPF</strong></summary>

```python
fw.ppf_maturity(yearly, rate, years)
fw.ppf_extension(current_balance, yearly, rate, extension_years)
fw.nps_maturity(monthly, rate, years, annuity_percent)
fw.nps_tax_benefit(contribution, employer_contribution, regime)
fw.epf_maturity(basic_da, rate, years, annual_increment)
```
</details>

<details>
<summary><strong>EMI & Gratuity</strong></summary>

```python
fw.emi(principal, rate, years)
fw.emi_amortization(principal, rate, years)
fw.emi_prepayment_impact(principal, rate, years, prepayment, prepay_after_months, strategy)
fw.gratuity(basic_da, years_of_service, employee_type)
```
</details>

<details>
<summary><strong>Salary & Planning</strong></summary>

```python
fw.hra_exemption(basic, hra_received, rent_paid, metro)
fw.ctc_to_inhand(ctc, regime)
fw.ssy_maturity(yearly, rate, deposit_years)
fw.lumpsum_maturity(amount, rate, years)
fw.future_cost(current_cost, inflation, years)
fw.retirement_corpus(monthly_expense, current_age, retirement_age)
```
</details>

<details>
<summary><strong>Stocks & Tax</strong></summary>

```python
fw.stock_pnl(buy_price, sell_price, quantity, trade_type)
fw.delivery_charges(buy_value, sell_value)
fw.intraday_charges(buy_value, sell_value)
fw.dividend_yield(annual_dividend, current_price)
fw.income_tax_slab(income, regime, fy)       # FY 2019-20 to 2024-25
fw.income_tax_compare(income, fy)            # old vs new regime
fw.stt(value, trade_type)
fw.gst_on_brokerage(brokerage)
fw.stamp_duty(value, instrument)
fw.tds_on_fd(interest, is_senior_citizen)
fw.tds_on_rd(interest, is_senior_citizen)
```
</details>

---

## Tax Rules Applied

| Rule | Implementation |
|------|---------------|
| Equity LTCG (>1 year) | 12.5% above ₹1.25L exemption |
| Equity STCG (≤1 year) | 20% flat |
| Debt MF (post Apr 2023) | Slab rate, no indexation |
| STT (delivery) | 0.1% on sell side |
| TDS on FD/RD | 10% above ₹40K (₹50K for senior citizens) |
| Income tax (new regime) | 0/5/10/15/20/30% slabs, ₹75K std deduction |
| Section 87A rebate | No tax up to ₹7L (new), ₹5L (old) |
| Surcharge | 10-37% based on income level |
| PPF | 7.1%, tax-free, 15-year lock-in |
| NPS | Min 40% annuity, 80CCD deductions |
| EPF | 8.1%, 12% employee + 3.67% employer |
| Gratuity | 15/26 formula, ₹20L tax-exempt cap |

---

## Contributing

PRs welcome. Roadmap:
- [ ] Gold/Silver returns (with import duty + GST)
- [ ] Crypto tax (30% flat + 1% TDS)
- [ ] Rental yield calculator
- [ ] Education loan with moratorium
- [ ] NPS Tier II
- [ ] Updated tax slabs for FY 2025-26

---

## Also Available

- **npm**: `npm install finworth` (TypeScript, works in React/React Native/Node.js) — *coming soon*
- **MCP Server**: `python -m finworth.mcp_server`

---

## License

MIT

---

Built by [Vikas Singh](https://github.com/vikisingh23)
