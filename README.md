# Competitive Intelligence Assistant

A focused PMM demo that monitors competitor webpages and turns changes into an actionable weekly brief.

> **Know what changed, why it matters, and what your GTM team should do next.**

## Two-minute demo

1. Open the Streamlit app.
2. Select **Two-minute demo mode**.
3. Click **Run weekly scan**.
4. Show the detected website changes.
5. Reveal the PMM brief: Observation → Inference → Action.

## What it does

- Crawls selected competitor pages
- Stores local snapshots
- Compares the latest snapshot with the prior run
- Sends the structured change data to the authenticated Claude Code CLI
- Produces a concise Markdown competitive brief

## Why it is PMM-specific

Traditional page monitors report raw text changes. This tool interprets changes through a GTM lens: positioning, audience, pricing, packaging, proof points, product capabilities, and sales enablement.

## Setup

```bash
cd competitive-intelligence-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
claude auth login --sso
streamlit run app.py
```

Claude Code officially supports non-interactive queries with `claude -p`. The app uses that command so the local Claude Code authentication handles model access; no API key is written into the repository.

## Testing

```bash
pytest
```

## Current scope

This MVP intentionally avoids dashboards, CRM integrations, social monitoring, and full battlecard generation. It is designed to communicate one clear PMM workflow in two minutes.
