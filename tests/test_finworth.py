"""Tests for finworth package."""

from datetime import date
import pytest
import finworth as fw


# === CORE ===

class TestXIRR:
    def test_simple_return(self):
        r = fw.xirr([(date(2020,1,1), -100000), (date(2021,1,1), 112000)])
        assert 0.11 < r < 0.13

    def test_multi_cashflow(self):
        r = fw.xirr([
            (date(2020,1,1), -50000),
            (date(2020,7,1), -50000),
            (date(2021,1,1), 115000),
        ])
        assert r > 0

    def test_negative_return(self):
        r = fw.xirr([(date(2020,1,1), -100000), (date(2021,1,1), 90000)])
        assert r < 0

    def test_empty(self):
        assert fw.xirr([]) == 0.0

    def test_single(self):
        assert fw.xirr([(date(2020,1,1), -100000)]) == 0.0


class TestCAGR:
    def test_doubling(self):
        r = fw.cagr(100000, 200000, 5)
        assert 0.148 < r < 0.149

    def test_zero_years(self):
        assert fw.cagr(100000, 200000, 0) == 0.0

    def test_zero_initial(self):
        assert fw.cagr(0, 200000, 5) == 0.0


class TestAbsoluteReturn:
    def test_positive(self):
        assert fw.absolute_return(100000, 120000) == 0.2

    def test_negative(self):
        assert fw.absolute_return(100000, 80000) == -0.2

    def test_zero_invested(self):
        assert fw.absolute_return(0, 100) == 0.0


class TestInflationAdjusted:
    def test_basic(self):
        r = fw.inflation_adjusted(0.12, 0.06)
        assert 0.056 < r < 0.057


# === MUTUAL FUNDS ===

class TestSIP:
    def test_basic(self):
        r = fw.sip_maturity(10000, 0.12, 10)
        assert r["invested"] == 1200000
        assert r["maturity"] > r["invested"]
        assert r["returns"] > 0

    def test_zero_rate(self):
        r = fw.sip_maturity(10000, 0, 5)
        assert r["maturity"] == r["invested"]


class TestSWP:
    def test_sustainable(self):
        r = fw.swp_projection(5000000, 30000, 0.08, 10)
        assert r["remaining_corpus"] > 0
        assert not r["corpus_exhausted"]

    def test_exhausted(self):
        r = fw.swp_projection(100000, 50000, 0.06, 5)
        assert r["corpus_exhausted"]


class TestMFCapitalGains:
    def test_equity_ltcg(self):
        r = fw.mf_capital_gains(100, 150, 1000, 400, "equity")
        assert r["gain_type"] == "LTCG"
        assert r["tax_rate"] == 0.125

    def test_equity_stcg(self):
        r = fw.mf_capital_gains(100, 150, 1000, 200, "equity")
        assert r["gain_type"] == "STCG"
        assert r["tax_rate"] == 0.20

    def test_debt(self):
        r = fw.mf_capital_gains(100, 120, 1000, 800, "debt")
        assert r["gain_type"] == "LTCG"
        assert r["tax_rate"] is None  # slab rate


# === FIXED DEPOSITS ===

class TestFD:
    def test_maturity(self):
        r = fw.fd_maturity(500000, 0.07, 3)
        assert r["maturity"] > 500000
        assert r["interest_earned"] > 0
        assert r["effective_rate"] > 0.07

    def test_post_tax(self):
        r = fw.fd_post_tax(500000, 0.07, 3, tax_slab=0.3)
        assert r["post_tax_maturity"] < r["pre_tax_maturity"]
        assert r["post_tax_rate"] < 0.07

    def test_compare(self):
        r = fw.fd_compare(500000, [
            {"bank": "SBI", "rate": 0.067},
            {"bank": "HDFC", "rate": 0.07},
        ], years=3)
        assert r[0]["bank"] == "HDFC"  # higher rate first


# === RECURRING DEPOSITS ===

class TestRD:
    def test_maturity(self):
        r = fw.rd_maturity(10000, 0.065, 5)
        assert r["invested"] == 600000
        assert r["maturity"] > 600000

    def test_effective_yield(self):
        r = fw.rd_effective_yield(0.065)
        assert r > 0.065


# === STOCKS ===

class TestStocks:
    def test_delivery_profit(self):
        r = fw.stock_pnl(100, 120, 100, "delivery")
        assert r["gross_pnl"] == 2000
        assert r["net_pnl"] < 2000  # charges deducted
        assert r["charges"]["stt"] > 0

    def test_delivery_loss(self):
        r = fw.stock_pnl(120, 100, 100, "delivery")
        assert r["gross_pnl"] == -2000

    def test_intraday(self):
        r = fw.stock_pnl(100, 105, 200, "intraday")
        assert r["charges"]["stt"] < fw.stock_pnl(100, 105, 200, "delivery")["charges"]["stt"]

    def test_dividend_yield(self):
        assert fw.dividend_yield(10, 500) == 0.02
        assert fw.dividend_yield(10, 0) == 0.0


# === TAX ===

class TestTax:
    def test_stt_delivery(self):
        assert fw.stt(100000, "equity_delivery") == 100.0

    def test_gst(self):
        assert fw.gst_on_brokerage(40) == 7.2

    def test_stamp_duty(self):
        assert fw.stamp_duty(100000, "equity_delivery") == 15.0

    def test_tds_below_limit(self):
        r = fw.tds_on_fd(30000)
        assert not r["tds_applicable"]

    def test_tds_above_limit(self):
        r = fw.tds_on_fd(60000)
        assert r["tds_applicable"]
        assert r["tds_amount"] == 6000.0

    def test_tds_senior_citizen(self):
        r = fw.tds_on_fd(45000, is_senior_citizen=True)
        assert not r["tds_applicable"]  # limit is 50K

    def test_income_tax_new_regime(self):
        r = fw.income_tax_slab(1500000, "new")
        assert r["total_tax"] > 0
        assert r["cess"] > 0

    def test_income_tax_rebate(self):
        r = fw.income_tax_slab(700000, "new")
        assert r["total_tax"] == 0  # 87A rebate

    def test_income_tax_old_regime(self):
        r = fw.income_tax_slab(1500000, "old")
        assert r["total_tax"] > 0


# === PPF ===

class TestPPF:
    def test_maturity_15_years(self):
        r = fw.ppf_maturity(150000, 0.071, 15)
        assert r["invested"] == 2250000
        assert r["maturity"] > 2250000
        assert len(r["yearly_breakdown"]) == 15

    def test_max_cap(self):
        r = fw.ppf_maturity(200000, 0.071, 15)  # should cap at 1.5L
        assert r["invested"] == 2250000

    def test_extension(self):
        base = fw.ppf_maturity(150000, 0.071, 15)
        ext = fw.ppf_extension(base["maturity"], 150000, 0.071, 5)
        assert ext["final_balance"] > base["maturity"]


# === NPS ===

class TestNPS:
    def test_maturity(self):
        r = fw.nps_maturity(5000, 0.10, 30)
        assert r["total_corpus"] > r["invested"]
        assert r["monthly_pension"] > 0
        assert r["annuity_percent"] >= 0.40

    def test_min_annuity(self):
        r = fw.nps_maturity(5000, 0.10, 30, annuity_percent=0.20)
        assert r["annuity_percent"] == 0.40  # forced to min 40%

    def test_tax_benefit_old(self):
        r = fw.nps_tax_benefit(200000, regime="old", tax_slab=0.3)
        assert r["sec_80ccd1"] == 150000
        assert r["sec_80ccd1b"] == 50000
        assert r["tax_saved"] > 0

    def test_tax_benefit_new(self):
        r = fw.nps_tax_benefit(200000, regime="new", tax_slab=0.3)
        assert r["sec_80ccd1b"] == 0  # no 1B in new regime


# === HISTORICAL TAX SLABS ===

class TestHistoricalTax:
    def test_old_regime_2019(self):
        r = fw.income_tax_slab(1000000, "old", "2019-20")
        assert r["fy"] == "2019-20"
        assert r["total_tax"] > 0

    def test_new_regime_2020(self):
        r = fw.income_tax_slab(1000000, "new", "2020-21")
        assert r["fy"] == "2020-21"
        assert r["standard_deduction"] == 0  # no std deduction in early new regime

    def test_new_regime_2023(self):
        r = fw.income_tax_slab(1000000, "new", "2023-24")
        assert r["standard_deduction"] == 50000

    def test_new_regime_2024(self):
        r = fw.income_tax_slab(1000000, "new", "2024-25")
        assert r["standard_deduction"] == 75000

    def test_rebate_old_regime(self):
        r = fw.income_tax_slab(500000, "old", "2022-23")
        assert r["total_tax"] == 0  # 87A rebate

    def test_rebate_new_regime_2024(self):
        r = fw.income_tax_slab(700000, "new", "2024-25")
        assert r["total_tax"] == 0  # 87A rebate up to 7L

    def test_compare_regimes(self):
        r = fw.income_tax_compare(1500000, "2024-25")
        assert "old_regime" in r
        assert "new_regime" in r
        assert r["recommendation"] in ("old", "new")

    def test_slab_breakdown(self):
        r = fw.income_tax_slab(2000000, "new", "2024-25")
        assert len(r["slab_breakdown"]) > 0
        assert all("slab" in s and "tax" in s for s in r["slab_breakdown"])

    def test_surcharge(self):
        r = fw.income_tax_slab(60000000, "new", "2024-25")
        assert r["surcharge"] > 0

    def test_invalid_fy(self):
        import pytest
        with pytest.raises(ValueError):
            fw.income_tax_slab(1000000, "new", "2018-19")


# === GRATUITY ===

class TestGratuity:
    def test_eligible(self):
        r = fw.gratuity(80000, 10)
        assert r["eligible"]
        assert r["gratuity_amount"] > 0
        assert r["completed_years"] == 10

    def test_not_eligible(self):
        r = fw.gratuity(80000, 3)
        assert not r["eligible"]

    def test_rounding_years(self):
        r = fw.gratuity(80000, 10.6)  # >6 months rounds up
        assert r["completed_years"] == 11

    def test_tax_exempt_cap(self):
        r = fw.gratuity(500000, 30)  # large gratuity
        assert r["tax_exempt"] <= 2000000


# === EMI ===

class TestEMI:
    def test_home_loan(self):
        r = fw.emi(5000000, 0.085, 20)
        assert r["emi"] > 0
        assert r["total_interest"] > 0
        assert r["total_payment"] == r["principal"] + r["total_interest"]

    def test_zero_rate(self):
        r = fw.emi(1200000, 0, 10)
        assert r["emi"] == 10000

    def test_amortization(self):
        schedule = fw.emi_amortization(5000000, 0.085, 20)
        assert len(schedule) == 20
        assert schedule[0]["interest_paid"] > schedule[0]["principal_paid"]  # early years interest-heavy
        assert schedule[-1]["balance"] == 0

    def test_prepayment_reduce_tenure(self):
        r = fw.emi_prepayment_impact(5000000, 0.085, 20, 500000, 24, "reduce_tenure")
        assert r["months_saved"] > 0
        assert r["interest_saved"] > 0

    def test_prepayment_reduce_emi(self):
        r = fw.emi_prepayment_impact(5000000, 0.085, 20, 500000, 24, "reduce_emi")
        assert r["new_emi"] < r["original_emi"]
        assert r["interest_saved"] > 0
