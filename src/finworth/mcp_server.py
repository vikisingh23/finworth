#!/usr/bin/env python3
"""finworth MCP server — exposes all financial calculators as MCP tools.

Run:
    python -m finworth.mcp_server

Add to .mcp.json:
    {
        "finworth": {
            "command": "python3",
            "args": ["-m", "finworth.mcp_server"]
        }
    }
"""

import json
import sys
from datetime import date
from finworth.ai import TOOL_REGISTRY


def read_message():
    header = ""
    while True:
        line = sys.stdin.readline()
        if line == "\r\n" or line == "\n":
            break
        header += line
    length = int(header.split("Content-Length:")[1].strip())
    body = sys.stdin.read(length)
    return json.loads(body)


def write_message(msg):
    body = json.dumps(msg)
    sys.stdout.write(f"Content-Length: {len(body)}\r\n\r\n{body}")
    sys.stdout.flush()


def build_tool_list():
    tools = []
    for t in TOOL_REGISTRY:
        tools.append({
            "name": t["name"],
            "description": t["description"],
            "inputSchema": {
                "type": "object",
                "properties": t["parameters"],
                "required": t["required"],
            },
        })
    # Add workflows
    tools.append({
        "name": "financial_health_check",
        "description": "Complete financial health check — CTC to retirement readiness in one call. Chains salary breakup, tax optimization, EPF, NPS, gratuity, retirement gap analysis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ctc": {"type": "number", "description": "Annual CTC in INR"},
                "age": {"type": "integer", "description": "Current age"},
                "monthly_rent": {"type": "number", "description": "Monthly rent (0 if own house)", "default": 0},
                "metro": {"type": "boolean", "description": "Metro city", "default": True},
                "nps_monthly": {"type": "number", "description": "Monthly NPS contribution", "default": 0},
                "home_loan_principal": {"type": "number", "description": "Outstanding home loan", "default": 0},
            },
            "required": ["ctc", "age"],
        },
    })
    tools.append({
        "name": "investment_compare",
        "description": "Compare same amount across Equity MF, Debt MF, FD, RD, PPF, NPS, EPF — sorted by post-tax returns.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "monthly": {"type": "number", "description": "Monthly investment amount"},
                "years": {"type": "integer", "description": "Investment horizon in years"},
                "tax_slab": {"type": "number", "description": "Income tax slab rate", "default": 0.3},
            },
            "required": ["monthly", "years"],
        },
    })
    return tools


def handle_call(name, args):
    from finworth.ai import execute
    from finworth.workflows import financial_health_check, investment_compare

    # Handle date conversion for xirr
    if name == "xirr" and "cashflows" in args:
        converted = []
        for cf in args["cashflows"]:
            d = date.fromisoformat(cf[0]) if isinstance(cf[0], str) else cf[0]
            converted.append((d, cf[1]))
        args["cashflows"] = converted

    if name == "financial_health_check":
        return financial_health_check(**args)
    elif name == "investment_compare":
        return investment_compare(**args)
    else:
        return execute(name, **args)


def main():
    while True:
        try:
            msg = read_message()
        except (EOFError, KeyboardInterrupt):
            break

        method = msg.get("method")
        id = msg.get("id")

        if method == "initialize":
            write_message({
                "jsonrpc": "2.0", "id": id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": "finworth", "version": "0.6.0"},
                },
            })
        elif method == "notifications/initialized":
            pass
        elif method == "tools/list":
            write_message({
                "jsonrpc": "2.0", "id": id,
                "result": {"tools": build_tool_list()},
            })
        elif method == "tools/call":
            name = msg["params"]["name"]
            args = msg["params"].get("arguments", {})
            try:
                result = handle_call(name, args)
                write_message({
                    "jsonrpc": "2.0", "id": id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, default=str)}]},
                })
            except Exception as e:
                write_message({
                    "jsonrpc": "2.0", "id": id,
                    "result": {"content": [{"type": "text", "text": f"Error: {str(e)}"}], "isError": True},
                })
        else:
            write_message({"jsonrpc": "2.0", "id": id, "result": {}})


if __name__ == "__main__":
    main()
