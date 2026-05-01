# finworth

Indian financial calculators for Python. Mutual Funds, Stocks, FD, RD — with accurate tax, charges, and regulatory rules.

```
pip install finworth
```

Zero dependencies. Pure Python. Works everywhere.

---

## What's Inside

| Module | What it calculates |
|--------|-------------------|
| **Core** | XIRR, CAGR, absolute return, inflation-adjusted return |
| **Mutual Funds** | SIP maturity, SWP projection, capital gains (LTCG/STCG with ₹1.25L exemption) |
| **Fixed Deposits** | Maturity (compound interest), post-tax returns, FD comparison |
| **Recurring Deposits** | Maturity (quarterly compounding), effective yield |
| **Stocks** | P&L with all charges (STT, GST, stamp duty, SEBI fees, DP charges), dividend yield |
| **Tax** | STT, GST on brokerage, stamp duty, TDS on FD/RD, income tax slabs (old + new regime) |

All calculations follow **Indian tax rules (FY 2024-25)** — SEBI, NSE/BSE charge structures, and Income Tax Act.

---

## Quick Start

```python
import finworth as fw
from datetime import date

# XIRR on any cashflows
fw.xirr([(date(2021,1,1), -100000), (date(2024,1,1), 145000)])
# → 0.1318 (13.18% annualized)

# SIP — ₹10K/month at 12% for 10 years
fw.sip_maturity(10000, 0.12, 10)
# → {'invested': 1200000, 'returns': 1123391, 'maturity': 2323391}

# FD — ₹5L at 7% for 3 years
fw.fd_maturity(500000, 0.07, 3)
# → {'principal': 500000, 'maturity': 615720, 'interest_earned': 115720}

# Stock P&L with all charges
fw.stock_pnl(500, 580, 200, "delivery")
# → {'gross_pnl': 16000, 'net_pnl': 15798.08, 'charges': {...}}

# Income tax (new regime)
fw.income_tax_slab(1500000, "new")
# → {'total_tax': 130000, 'effective_rate': 0.086667}
```

---

## All Functions

### Core

```python
# XIRR — works with any irregular cashflows
fw.xirr([(date, amount), ...])

# CAGR
fw.cagr(initial=100000, final=200000, years=5)  # → 0.1487

# Absolute return
fw.absolute_return(invested=100000, current=120000)  # → 0.2

# Inflation-adjusted (real) return
fw.inflation_adjusted(nominal_return=0.12, inflation=0.06)  # → 0.0566
```

### Mutual Funds

```python
# SIP future value
fw.sip_maturity(monthly=10000, rate=0.12, years=10)

# SIP XIRR (running SIP)
fw.sip_xirr(monthly=10000, current_value=850000, months=60)

# SWP projection
fw.swp_projection(corpus=5000000, monthly_withdrawal=30000, rate=0.08, years=20)

# Capital gains (equity — with ₹1.25L LTCG exemption)
fw.mf_capital_gains(buy_nav=100, sell_nav=180, units=500, holding_days=400, fund_type="equity")

# Capital gains (debt — slab rate, no indexation post Apr 2023)
fw.mf_capital_gains(buy_nav=100, sell_nav=120, units=1000, holding_days=800, fund_type="debt")
```

### Fixed Deposits

```python
# Maturity amount
fw.fd_maturity(principal=500000, rate=0.07, years=3, compounding="quarterly")

# Post-tax returns
fw.fd_post_tax(principal=500000, rate=0.07, years=3, tax_slab=0.3)

# Compare FDs across banks
fw.fd_compare(500000, [
    {"bank": "SBI", "rate": 0.067},
    {"bank": "HDFC", "rate": 0.070},
    {"bank": "Post Office", "rate": 0.074},
], years=3)
```

### Recurring Deposits

```python
# RD maturity (quarterly compounding)
fw.rd_maturity(monthly=10000, rate=0.065, years=5)

# Effective annual yield
fw.rd_effective_yield(rate=0.065)  # → 0.066
```

### Stocks

```python
# Delivery trade P&L with all charges
fw.stock_pnl(buy_price=500, sell_price=580, quantity=200, trade_type="delivery")

# Intraday trade
fw.stock_pnl(buy_price=500, sell_price=510, quantity=200, trade_type="intraday")

# Dividend yield
fw.dividend_yield(annual_dividend=10, current_price=500)  # → 0.02

# Just the charges
fw.delivery_charges(buy_value=100000, sell_value=116000)
fw.intraday_charges(buy_value=100000, sell_value=101000)
```

### Tax

```python
# Income tax — new regime (FY 2024-25)
fw.income_tax_slab(income=1500000, regime="new")

# Income tax — old regime
fw.income_tax_slab(income=1500000, regime="old")

# STT
fw.stt(value=100000, trade_type="equity_delivery")  # → 100.0

# GST on brokerage
fw.gst_on_brokerage(brokerage=40)  # → 7.2

# Stamp duty
fw.stamp_duty(value=100000, instrument="equity_delivery")  # → 15.0

# TDS on FD interest
fw.tds_on_fd(interest=60000)  # → {'tds_amount': 6000, ...}
fw.tds_on_fd(interest=45000, is_senior_citizen=True)  # → no TDS (₹50K limit)
```

---

## Tax Rules Applied

| Rule | Implementation |
|------|---------------|
| Equity LTCG (>1 year) | 12.5% above ₹1.25L exemption |
| Equity STCG (≤1 year) | 20% flat |
| Debt MF (post Apr 2023) | Slab rate, no indexation |
| STT (delivery) | 0.1% on sell side |
| STT (intraday) | 0.025% on sell side |
| TDS on FD/RD | 10% above ₹40K (₹50K for senior citizens) |
| Income tax (new regime) | 0/5/10/15/20/30% slabs with ₹75K standard deduction |
| Section 87A rebate | No tax up to ₹7L taxable income (new regime) |
| Stamp duty | 0.015% delivery, 0.003% intraday |

---

## Examples

See [`examples.py`](examples.py) for a complete walkthrough with formatted output.

```bash
python examples.py
```

---

## Contributing

PRs welcome. If you want to add:
- **NPS calculator** — go for it
- **PPF calculator** — yes please
- **Gold/Silver returns** — with import duty and GST
- **Crypto tax** — 30% flat + 1% TDS
- **Updated tax slabs** — for new financial years

---

## License

MIT

---

Built by [Vikas Singh](https://github.com/vikisingh23)
