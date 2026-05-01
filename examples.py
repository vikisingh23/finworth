"""finworth examples — run with: python examples.py"""

from datetime import date
import finworth as fw

print("=" * 60)
print("finworth — Indian Financial Calculator Examples")
print("=" * 60)

# ── XIRR ──────────────────────────────────────────────────
print("\n📊 XIRR — Portfolio Return")
cashflows = [
    (date(2021, 1, 15), -100000),   # invested 1L
    (date(2021, 7, 10), -50000),    # invested 50K more
    (date(2022, 3, 20), -25000),    # invested 25K more
    (date(2024, 1, 15), 250000),    # current value 2.5L
]
print(f"  XIRR: {fw.xirr(cashflows) * 100:.2f}%")

# ── SIP ───────────────────────────────────────────────────
print("\n💰 SIP — ₹10,000/month at 12% for 10 years")
sip = fw.sip_maturity(10000, 0.12, 10)
print(f"  Invested:  ₹{sip['invested']:,.0f}")
print(f"  Returns:   ₹{sip['returns']:,.0f}")
print(f"  Maturity:  ₹{sip['maturity']:,.0f}")

# ── SWP ───────────────────────────────────────────────────
print("\n📤 SWP — ₹50L corpus, ₹30K/month withdrawal at 8%")
swp = fw.swp_projection(5000000, 30000, 0.08, 20)
print(f"  Withdrawn:  ₹{swp['total_withdrawn']:,.0f}")
print(f"  Remaining:  ₹{swp['remaining_corpus']:,.0f}")
print(f"  Exhausted:  {swp['corpus_exhausted']}")

# ── MF Capital Gains ──────────────────────────────────────
print("\n📈 MF Capital Gains — Equity LTCG")
cg = fw.mf_capital_gains(buy_nav=100, sell_nav=180, units=500, holding_days=400, fund_type="equity")
print(f"  Gain:      ₹{cg['gain']:,.0f} ({cg['gain_type']})")
print(f"  Taxable:   ₹{cg['taxable_gain']:,.0f} (after ₹1.25L exemption)")
print(f"  Tax:       ₹{cg['tax_amount']:,.0f} at {cg['tax_rate']*100}%")

# ── Fixed Deposit ─────────────────────────────────────────
print("\n🏦 FD — ₹5L at 7% for 3 years")
fd = fw.fd_maturity(500000, 0.07, 3)
print(f"  Maturity:  ₹{fd['maturity']:,.0f}")
print(f"  Interest:  ₹{fd['interest_earned']:,.0f}")
print(f"  Eff Rate:  {fd['effective_rate']*100:.2f}%")

print("\n🏦 FD Post-Tax (30% slab)")
fd_tax = fw.fd_post_tax(500000, 0.07, 3, tax_slab=0.3)
print(f"  Post-tax:  ₹{fd_tax['post_tax_maturity']:,.0f}")
print(f"  Post Rate: {fd_tax['post_tax_rate']*100:.2f}%")

print("\n🏦 FD Compare")
comparison = fw.fd_compare(500000, [
    {"bank": "SBI", "rate": 0.067},
    {"bank": "HDFC", "rate": 0.070},
    {"bank": "Post Office", "rate": 0.074},
], years=3)
for c in comparison:
    print(f"  {c['bank']:15s} → ₹{c['maturity']:,.0f} ({c['effective_rate']*100:.2f}%)")

# ── Recurring Deposit ─────────────────────────────────────
print("\n🔄 RD — ₹10,000/month at 6.5% for 5 years")
rd = fw.rd_maturity(10000, 0.065, 5)
print(f"  Invested:  ₹{rd['invested']:,.0f}")
print(f"  Maturity:  ₹{rd['maturity']:,.0f}")
print(f"  Interest:  ₹{rd['interest_earned']:,.0f}")

# ── Stock Trading ─────────────────────────────────────────
print("\n📉 Stock — Buy ₹500 × 200 shares, Sell ₹580 (Delivery)")
pnl = fw.stock_pnl(500, 580, 200, "delivery")
print(f"  Gross P&L: ₹{pnl['gross_pnl']:,.0f}")
print(f"  Charges:   ₹{pnl['charges']['total_charges']:,.2f}")
print(f"    STT:     ₹{pnl['charges']['stt']:,.2f}")
print(f"    GST:     ₹{pnl['charges']['gst']:,.2f}")
print(f"    Stamp:   ₹{pnl['charges']['stamp_duty']:,.2f}")
print(f"  Net P&L:   ₹{pnl['net_pnl']:,.2f}")
print(f"  Return:    {pnl['effective_return']*100:.2f}%")

print("\n📉 Stock — Intraday ₹500 × 200 shares, Sell ₹510")
pnl2 = fw.stock_pnl(500, 510, 200, "intraday")
print(f"  Gross P&L: ₹{pnl2['gross_pnl']:,.0f}")
print(f"  Charges:   ₹{pnl2['charges']['total_charges']:,.2f}")
print(f"  Net P&L:   ₹{pnl2['net_pnl']:,.2f}")

# ── Income Tax ────────────────────────────────────────────
print("\n🧾 Income Tax — ₹15L (New Regime)")
tax = fw.income_tax_slab(1500000, "new")
print(f"  Taxable:   ₹{tax['taxable_income']:,.0f}")
print(f"  Tax:       ₹{tax['tax_before_cess']:,.0f}")
print(f"  Cess:      ₹{tax['cess']:,.0f}")
print(f"  Total:     ₹{tax['total_tax']:,.0f}")
print(f"  Effective: {tax['effective_rate']*100:.2f}%")

print("\n🧾 Income Tax — ₹7L (New Regime, 87A Rebate)")
tax2 = fw.income_tax_slab(700000, "new")
print(f"  Total Tax: ₹{tax2['total_tax']:,.0f} (rebate applied)")

# ── TDS ───────────────────────────────────────────────────
print("\n💳 TDS on FD — ₹60K interest")
tds = fw.tds_on_fd(60000)
print(f"  TDS:       ₹{tds['tds_amount']:,.0f}")
print(f"  Net:       ₹{tds['net_interest']:,.0f}")

print("\n" + "=" * 60)
print("Done! Install: pip install finworth")
print("=" * 60)
