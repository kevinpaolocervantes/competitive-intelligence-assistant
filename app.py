from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from src.claude_analyzer import analyze_with_claude, claude_available, demo_brief
from src.crawler import crawl_urls
from src.diffing import compare_runs
from src.storage import load_history, save_run

st.set_page_config(page_title="Competitive Intelligence Assistant", page_icon="🔎", layout="wide")

st.title("Competitive Intelligence Assistant")
st.caption("Monitor competitor websites and turn meaningful changes into an actionable weekly PMM brief.")

with st.sidebar:
    st.header("Monitor a competitor")
    competitor = st.text_input("Competitor name", value="Adobe")
    urls_raw = st.text_area(
        "Pages to monitor (one URL per line)",
        value="https://www.adobe.com/\nhttps://www.adobe.com/products/catalog.html",
        height=130,
    )
    mode = st.radio("Analysis mode", ["Live crawl + Claude Code", "Two-minute demo mode"])
    run_scan = st.button("Run weekly scan", type="primary", use_container_width=True)
    st.divider()
    st.write("Claude Code status:", "✅ Available" if claude_available() else "⚠️ Not detected")
    st.caption("Live analysis uses `claude -p` and your existing Claude Code login—no API key is stored in this app.")

if run_scan:
    if not competitor.strip():
        st.error("Enter a competitor name.")
    elif mode == "Two-minute demo mode":
        st.session_state["brief"] = demo_brief(competitor)
        st.session_state["changes"] = [
            {"url": "Homepage", "status": "changed", "summary": "Primary message changed to AI-led enterprise outcomes."},
            {"url": "Security", "status": "new_page", "summary": "New enterprise security and governance page."},
            {"url": "Pricing", "status": "changed", "summary": "Self-service pricing replaced by contact sales."},
        ]
        st.success("Demo scan complete: 3 meaningful changes detected.")
    else:
        urls = [line.strip() for line in urls_raw.splitlines() if line.strip()]
        try:
            with st.spinner("Crawling pages and comparing snapshots..."):
                pages = [snapshot.to_dict() for snapshot in crawl_urls(urls)]
                current = {
                    "captured_at": datetime.now(timezone.utc).isoformat(),
                    "pages": pages,
                }
                history = load_history(competitor)
                previous = history[-1] if history else None
                changes = compare_runs(previous, current)
                save_run(competitor, current)
            with st.spinner("Claude Code is interpreting the GTM implications..."):
                brief = analyze_with_claude(competitor, changes)
            st.session_state["changes"] = changes
            st.session_state["brief"] = brief
            st.success(f"Scan complete: {len(changes)} noteworthy page results.")
        except Exception as exc:
            st.error(str(exc))

changes = st.session_state.get("changes", [])
brief = st.session_state.get("brief")

if changes:
    st.subheader("Detected changes")
    cols = st.columns(min(3, len(changes)))
    for index, change in enumerate(changes):
        with cols[index % len(cols)]:
            st.metric(change["status"].replace("_", " ").title(), change["summary"])
            st.caption(change["url"])

if brief:
    st.subheader("Generated PMM brief")
    st.markdown(brief)
    st.download_button(
        "Download Markdown brief",
        data=brief,
        file_name=f"{competitor.lower().replace(' ', '-')}-weekly-brief.md",
        mime="text/markdown",
    )
else:
    st.info("Run the demo mode first to see the full two-minute experience without crawling a live site.")
