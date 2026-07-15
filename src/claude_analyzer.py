from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any

SYSTEM_GUIDANCE = """You are a senior B2B SaaS product marketing manager specializing in competitive intelligence.
Analyze website changes conservatively. Separate direct observation from inference. Do not invent motives.
Return concise Markdown with exactly these sections:
# Weekly Competitive Brief
## Executive Summary
## Observations
## GTM Implications
## Recommended Actions
## Evidence and Confidence
For each important item, explicitly label Observation, Inference, Action, and Confidence (High/Medium/Low).
Prioritize changes to positioning, target audience, pricing, packaging, product capabilities, proof points, and sales enablement.
"""


def claude_available() -> bool:
    return shutil.which("claude") is not None


def analyze_with_claude(competitor: str, changes: list[dict[str, str]]) -> str:
    if not claude_available():
        raise RuntimeError("Claude Code CLI was not found. Install it and run `claude auth login --sso`.")

    prompt = f"""{SYSTEM_GUIDANCE}

Competitor: {competitor}
Website change data:
{json.dumps(changes, indent=2)[:80_000]}

Generate the brief now. If this is only a baseline snapshot, say that no week-over-week inference is possible yet.
"""
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Claude Code analysis failed.")
    return result.stdout.strip()


def demo_brief(competitor: str) -> str:
    return f"""# Weekly Competitive Brief

## Executive Summary
{competitor} appears to be sharpening its enterprise AI narrative. The most important signal is a shift from broad productivity language toward security, governance, and measurable business outcomes.

## Observations
- **Observation:** AI-led messaging moved into the primary homepage headline.
- **Observation:** A new enterprise security page was added.
- **Observation:** Transparent pricing was replaced with a contact-sales motion.

## GTM Implications
- **Inference:** The competitor may be moving further upmarket. **Confidence: Medium**
- **Inference:** Trust and governance are becoming more important parts of its differentiation. **Confidence: High**

## Recommended Actions
- **Action:** Review the enterprise battlecard and add a direct response to the new security narrative.
- **Action:** Brief sales on the pricing-page change before the next enablement session.
- **Action:** Monitor customer proof and vertical case studies in the next scan.

## Evidence and Confidence
This demo report uses seeded sample changes. Connect the authenticated Claude Code CLI and run two real snapshots for evidence-backed analysis.
"""
