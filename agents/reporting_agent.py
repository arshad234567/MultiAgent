"""
agents/reporting_agent.py

Fast reporting agent (no LLM dependency needed for speed).
"""

def reporting_agent(breach, position, analysis):
    report = {
        "summary": f"{breach['symbol']} exceeded risk limit by {breach['breach_pct']}%.",
        "root_cause": analysis.get("cause"),
        "recurrence_risk": "high" if breach["breach_pct"] > 50 else "medium",
        "recommended_actions": [
            "Reduce exposure",
            "Rebalance portfolio",
            "Review risk limits"
        ]
    }

    return report


def format_report(breach, analysis, report):
    actions = "\n".join(f"  • {a}" for a in report["recommended_actions"])

    return f"""
════════════════════════════════════════════════════
   BREACH MONITOR AI — INVESTIGATION REPORT
════════════════════════════════════════════════════

SYMBOL      : {breach['symbol']}
SEVERITY    : {analysis.get('severity')}
BREACH %    : {breach['breach_pct']}%
VALUE       : {breach['value']:.2f}
LIMIT       : {breach['limit']:.2f}

SUMMARY:
{report['summary']}

ROOT CAUSE:
{report['root_cause']}

RECURRENCE RISK:
{report['recurrence_risk']}

RECOMMENDED ACTIONS:
{actions}

════════════════════════════════════════════════════
""".strip()