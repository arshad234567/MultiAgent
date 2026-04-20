"""
agents/reasoning_agent.py
reasoning agent using Ollama.
Includes:
- strict prompting
- JSON extraction
- validation
- fallback logic
"""

import requests
import json
import re
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
CONFIDENCE_THRESHOLD = 0.7


def reasoning_agent(breach, position):
    breach_pct = breach["breach_pct"]

    # Skipping LLM for low risk
    if breach_pct < 20:
        return {
            "severity": "LOW",
            "risk_type": "minor exposure",
            "cause": f"small breach of {breach_pct}%",
            "recommendation": "Monitor position",
            "confidence": 0.85
        }

    # Medium risk rule-based
    if breach_pct < 30:
        return {
            "severity": "MEDIUM",
            "risk_type": "moderate exposure",
            "cause": f"Exposure exceeded limit by {breach_pct}%",
            "recommendation": "Rebalance portfolio",
            "confidence": 0.75
        }

    # LLM prompt
    prompt = f"""
You are a financial risk analyst.

This is a portfolio VALUE breach (not stock price, not cybersecurity).

Analyze ONLY financial exposure risk.

Data:
Symbol: {breach['symbol']}
Position Value: {breach['value']}
Limit: {breach['limit']}
Breach: {breach['breach_pct']}%
Weight: {position['weight']}

Rules:
- Focus on position value exceeding limit
- DO NOT mention stock price movement
- DO NOT mention hacking/security
- Use financial terms: exposure, allocation, concentration

Return ONLY JSON:

{{
  "severity": "HIGH|MEDIUM|LOW",
  "risk_type": "concentration risk | exposure breach",
  "cause": "clear explanation using value vs limit",
  "recommendation": "actionable portfolio step",
  "confidence": 0-1
}}
"""

    try:
        start = time.time()

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        latency = time.time() - start

        # Skip slow LLM
        if latency > 15:
            raise TimeoutError("LLM too slow")

        raw = response.json()["response"].strip()

        #  Extract JSON safely
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError("No JSON found")

        clean_json = match.group(0)
        analysis = json.loads(clean_json)

        #  Validate output
        if not isinstance(analysis.get("cause"), str):
            raise ValueError("Invalid format")

        if "price" in analysis.get("cause", "").lower():
            raise ValueError("Invalid reasoning (mentions price)")

    except Exception as e:
        print(f"[Reasoning FALLBACK] {breach['symbol']} → {str(e)}")

        # Fallback for high risk
        analysis = {
            "severity": "HIGH",
            "risk_type": "concentration risk",
            "cause": f"Critical breach of {breach_pct}%",
            "recommendation": "Immediate reduction required",
            "confidence": 0.6
        }

    # severity correction
    if breach_pct < 15:
        analysis["severity"] = "LOW"
    elif breach_pct < 30:
        analysis["severity"] = "MEDIUM"
    elif breach_pct < 60:
        analysis["severity"] = "MEDIUM"
    else:
        analysis["severity"] = "HIGH"

    print(
        f"[Reasoning] {breach['symbol']} | "
        f"Severity: {analysis.get('severity')} | "
        f"Confidence: {analysis.get('confidence', 0):.0%}"
    )

    return analysis