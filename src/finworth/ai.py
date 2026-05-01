"""AI agent integration — tool registry, schemas, and natural language mapping.

Usage with LangChain:
    from finworth.ai import get_tools
    tools = get_tools()  # returns list of tool definitions

Usage with OpenAI function calling:
    from finworth.ai import get_openai_functions
    functions = get_openai_functions()  # returns OpenAI-compatible function schemas

Usage with plain lookup:
    from finworth.ai import find_tool
    tool = find_tool("how much will my SIP give me")
    result = tool["fn"](monthly=10000, rate=0.12, years=10)
"""

from __future__ import annotations
import finworth as fw

TOOL_REGISTRY = [
    {
        "name": "xirr",
        "fn": fw.xirr,
        "description": "Calculate XIRR (annualized return) for irregular cashflows. Use when user has multiple investments/withdrawals at different dates.",
        "keywords": ["xirr", "return", "portfolio return", "annualized", "irr", "cashflow"],
        "parameters": {
            "cashflows": {"type": "array", "items": {"type": "array", "description": "[date, amount]"}, "description": "List of [date, amount] tuples. Negative=investment, positive=redemption."},
        },
        "required": ["cashflows"],
        "example": "xirr([(date(2020,1,1), -100000), (date(2023,1,1), 145000)])",
    },
    {
        "name": "sip_maturity",
        "fn": fw.sip_maturity,
        "description": "Calculate future value of a monthly SIP investment. Use when user asks about SIP returns, SIP calculator, or monthly investment growth.",
        "keywords": ["sip", "monthly investment", "systematic investment", "sip calculator", "sip returns", "mutual fund sip"],
        "parameters": {
            "monthly": {"type": "number", "description": "Monthly SIP amount in INR"},
            "rate": {"type": "number", "description": "Expected annual return as decimal (0.12 = 12%)"},
            "years": {"type": "integer", "description": "Investment duration in years"},
        },
        "required": ["monthly", "rate", "years"],
    },
    {
        "name": "lumpsum_maturity",
        "fn": fw.lumpsum_maturity,
        "description": "Calculate future value of a one-time investment. Use for lumpsum mutual fund or equity investment.",
        "keywords": ["lumpsum", "one time investment", "future value", "compound interest"],
        "parameters": {
            "amount": {"type": "number", "description": "One-time investment amount"},
            "rate": {"type": "number", "description": "Expected annual return as decimal"},
            "years": {"type": "integer", "description": "Investment horizon in years"},
        },
        "required": ["amount", "rate", "years"],
    },
    {
        "name": "fd_maturity",
        "fn": fw.fd_maturity,
        "description": "Calculate Fixed Deposit maturity amount with compound interest. Use for FD calculator queries.",
        "keywords": ["fd", "fixed deposit", "fd calculator", "fd maturity", "fd interest", "bank fd"],
        "parameters": {
            "principal": {"type": "number", "description": "Deposit amount in INR"},
            "rate": {"type": "number", "description": "Annual interest rate as decimal (0.07 = 7%)"},
            "years": {"type": "number", "description": "Tenure in years"},
            "compounding": {"type": "string", "enum": ["quarterly", "monthly", "half-yearly", "yearly"], "default": "quarterly"},
        },
        "required": ["principal", "rate", "years"],
    },
    {
        "name": "rd_maturity",
        "fn": fw.rd_maturity,
        "description": "Calculate Recurring Deposit maturity amount. Use for RD calculator queries.",
        "keywords": ["rd", "recurring deposit", "rd calculator", "rd maturity"],
        "parameters": {
            "monthly": {"type": "number", "description": "Monthly deposit amount"},
            "rate": {"type": "number", "description": "Annual interest rate as decimal"},
            "years": {"type": "integer", "description": "Tenure in years"},
        },
        "required": ["monthly", "rate", "years"],
    },
    {
        "name": "ppf_maturity",
        "fn": fw.ppf_maturity,
        "description": "Calculate PPF (Public Provident Fund) maturity. 15-year lock-in, tax-free returns.",
        "keywords": ["ppf", "public provident fund", "ppf calculator", "ppf maturity", "ppf interest"],
        "parameters": {
            "yearly": {"type": "number", "description": "Annual contribution (max 1.5L)"},
            "rate": {"type": "number", "description": "PPF interest rate (default 7.1%)", "default": 0.071},
            "years": {"type": "integer", "description": "Duration (default 15)", "default": 15},
        },
        "required": ["yearly"],
    },
    {
        "name": "nps_maturity",
        "fn": fw.nps_maturity,
        "description": "Calculate NPS (National Pension System) corpus and monthly pension at retirement.",
        "keywords": ["nps", "national pension", "pension", "nps calculator", "retirement pension"],
        "parameters": {
            "monthly": {"type": "number", "description": "Monthly NPS contribution"},
            "rate": {"type": "number", "description": "Expected return (default 10%)", "default": 0.10},
            "years": {"type": "integer", "description": "Years until retirement"},
        },
        "required": ["monthly", "years"],
    },
    {
        "name": "epf_maturity",
        "fn": fw.epf_maturity,
        "description": "Calculate EPF (Employee Provident Fund) corpus at retirement with employer match.",
        "keywords": ["epf", "pf", "provident fund", "epf calculator", "pf balance"],
        "parameters": {
            "basic_da": {"type": "number", "description": "Monthly Basic + DA salary"},
            "rate": {"type": "number", "description": "EPF interest rate (default 8.1%)", "default": 0.081},
            "years": {"type": "integer", "description": "Years until retirement"},
        },
        "required": ["basic_da", "years"],
    },
    {
        "name": "emi",
        "fn": fw.emi,
        "description": "Calculate EMI for home loan, personal loan, or car loan.",
        "keywords": ["emi", "loan emi", "home loan", "personal loan", "car loan", "emi calculator", "monthly installment"],
        "parameters": {
            "principal": {"type": "number", "description": "Loan amount"},
            "rate": {"type": "number", "description": "Annual interest rate as decimal (0.085 = 8.5%)"},
            "years": {"type": "integer", "description": "Loan tenure in years"},
        },
        "required": ["principal", "rate", "years"],
    },
    {
        "name": "income_tax_slab",
        "fn": fw.income_tax_slab,
        "description": "Calculate Indian income tax with slab-wise breakdown. Supports old and new regime, FY 2019-20 to 2024-25.",
        "keywords": ["income tax", "tax calculator", "tax slab", "old regime", "new regime", "tax on salary"],
        "parameters": {
            "income": {"type": "number", "description": "Total taxable income"},
            "regime": {"type": "string", "enum": ["old", "new"], "default": "new"},
            "fy": {"type": "string", "description": "Financial year (2019-20 to 2024-25)", "default": "2024-25"},
        },
        "required": ["income"],
    },
    {
        "name": "income_tax_compare",
        "fn": fw.income_tax_compare,
        "description": "Compare old vs new tax regime and recommend the better option.",
        "keywords": ["old vs new regime", "which regime", "tax comparison", "regime comparison"],
        "parameters": {
            "income": {"type": "number", "description": "Total taxable income"},
            "fy": {"type": "string", "default": "2024-25"},
        },
        "required": ["income"],
    },
    {
        "name": "hra_exemption",
        "fn": fw.hra_exemption,
        "description": "Calculate HRA tax exemption under Section 10(13A).",
        "keywords": ["hra", "hra exemption", "hra calculator", "house rent allowance", "hra tax benefit"],
        "parameters": {
            "basic": {"type": "number", "description": "Monthly basic salary"},
            "hra_received": {"type": "number", "description": "Monthly HRA received"},
            "rent_paid": {"type": "number", "description": "Monthly rent paid"},
            "metro": {"type": "boolean", "description": "True for Delhi/Mumbai/Kolkata/Chennai", "default": True},
        },
        "required": ["basic", "hra_received", "rent_paid"],
    },
    {
        "name": "ctc_to_inhand",
        "fn": fw.ctc_to_inhand,
        "description": "Convert CTC to monthly in-hand salary with full breakup (basic, HRA, PF, tax).",
        "keywords": ["ctc", "in hand salary", "take home", "salary breakup", "ctc calculator", "net salary"],
        "parameters": {
            "ctc": {"type": "number", "description": "Annual CTC in INR"},
            "regime": {"type": "string", "enum": ["old", "new"], "default": "new"},
        },
        "required": ["ctc"],
    },
    {
        "name": "gratuity",
        "fn": fw.gratuity,
        "description": "Calculate gratuity amount under Payment of Gratuity Act (min 5 years service).",
        "keywords": ["gratuity", "gratuity calculator", "gratuity amount", "retirement gratuity"],
        "parameters": {
            "basic_da": {"type": "number", "description": "Last drawn monthly Basic + DA"},
            "years_of_service": {"type": "number", "description": "Total years of service"},
        },
        "required": ["basic_da", "years_of_service"],
    },
    {
        "name": "ssy_maturity",
        "fn": fw.ssy_maturity,
        "description": "Calculate Sukanya Samriddhi Yojana maturity (girl child savings scheme, 21-year maturity).",
        "keywords": ["ssy", "sukanya samriddhi", "girl child", "sukanya scheme"],
        "parameters": {
            "yearly": {"type": "number", "description": "Annual deposit (min 250, max 1.5L)"},
        },
        "required": ["yearly"],
    },
    {
        "name": "retirement_corpus",
        "fn": fw.retirement_corpus,
        "description": "Calculate how much corpus is needed for retirement and monthly SIP required to build it.",
        "keywords": ["retirement", "retirement planning", "retirement corpus", "how much to retire", "fire"],
        "parameters": {
            "monthly_expense": {"type": "number", "description": "Current monthly expense"},
            "current_age": {"type": "integer", "description": "Current age", "default": 30},
            "retirement_age": {"type": "integer", "description": "Planned retirement age", "default": 60},
        },
        "required": ["monthly_expense"],
    },
    {
        "name": "stock_pnl",
        "fn": fw.stock_pnl,
        "description": "Calculate stock trading P&L with all charges (STT, GST, stamp duty, brokerage).",
        "keywords": ["stock profit", "stock loss", "trading pnl", "brokerage charges", "stock charges"],
        "parameters": {
            "buy_price": {"type": "number", "description": "Buy price per share"},
            "sell_price": {"type": "number", "description": "Sell price per share"},
            "quantity": {"type": "integer", "description": "Number of shares"},
            "trade_type": {"type": "string", "enum": ["delivery", "intraday"], "default": "delivery"},
        },
        "required": ["buy_price", "sell_price", "quantity"],
    },
    {
        "name": "mf_capital_gains",
        "fn": fw.mf_capital_gains,
        "description": "Calculate mutual fund capital gains tax (LTCG/STCG) for equity and debt funds.",
        "keywords": ["capital gains", "ltcg", "stcg", "mutual fund tax", "redemption tax"],
        "parameters": {
            "buy_nav": {"type": "number", "description": "Purchase NAV"},
            "sell_nav": {"type": "number", "description": "Redemption NAV"},
            "units": {"type": "number", "description": "Number of units"},
            "holding_days": {"type": "integer", "description": "Days between buy and sell"},
            "fund_type": {"type": "string", "enum": ["equity", "debt"], "default": "equity"},
        },
        "required": ["buy_nav", "sell_nav", "units", "holding_days"],
    },
    {
        "name": "swp_projection",
        "fn": fw.swp_projection,
        "description": "Project how long a corpus will last with systematic withdrawals (SWP).",
        "keywords": ["swp", "systematic withdrawal", "withdrawal plan", "corpus withdrawal", "monthly income from investment"],
        "parameters": {
            "corpus": {"type": "number", "description": "Initial corpus amount"},
            "monthly_withdrawal": {"type": "number", "description": "Monthly withdrawal amount"},
            "rate": {"type": "number", "description": "Expected annual return"},
            "years": {"type": "integer", "description": "Projection period in years"},
        },
        "required": ["corpus", "monthly_withdrawal", "rate", "years"],
    },
    {
        "name": "future_cost",
        "fn": fw.future_cost,
        "description": "Calculate future cost of something due to inflation.",
        "keywords": ["inflation", "future cost", "inflation calculator", "price in future"],
        "parameters": {
            "current_cost": {"type": "number", "description": "Current cost/expense"},
            "inflation": {"type": "number", "description": "Expected inflation rate", "default": 0.06},
            "years": {"type": "integer", "description": "Years in future"},
        },
        "required": ["current_cost", "years"],
    },
]


def get_tools() -> list[dict]:
    """Get all tool definitions (for any AI framework)."""
    return TOOL_REGISTRY


def get_openai_functions() -> list[dict]:
    """Get OpenAI function-calling compatible schemas."""
    functions = []
    for tool in TOOL_REGISTRY:
        functions.append({
            "name": tool["name"],
            "description": tool["description"],
            "parameters": {
                "type": "object",
                "properties": tool["parameters"],
                "required": tool["required"],
            },
        })
    return functions


def find_tool(query: str) -> dict | None:
    """Find the best matching tool for a natural language query.

    Args:
        query: Natural language question like "how much will my SIP give me"

    Returns:
        Best matching tool dict with 'fn' callable, or None.

    Example:
        >>> tool = find_tool("calculate my home loan EMI")
        >>> tool["fn"](principal=5000000, rate=0.085, years=20)
    """
    query_lower = query.lower()
    best_match = None
    best_score = 0

    for tool in TOOL_REGISTRY:
        score = 0
        for kw in tool["keywords"]:
            if kw in query_lower:
                score += len(kw)  # longer keyword matches = higher confidence
        if tool["name"] in query_lower:
            score += 10
        if score > best_score:
            best_score = score
            best_match = tool

    return best_match if best_score > 0 else None


def execute(tool_name: str, **kwargs):
    """Execute a tool by name with given parameters.

    Args:
        tool_name: Function name from the registry.
        **kwargs: Parameters for the function.

    Returns:
        Function result (dict).

    Example:
        >>> execute("sip_maturity", monthly=10000, rate=0.12, years=10)
    """
    for tool in TOOL_REGISTRY:
        if tool["name"] == tool_name:
            return tool["fn"](**kwargs)
    raise ValueError(f"Tool '{tool_name}' not found. Available: {[t['name'] for t in TOOL_REGISTRY]}")
