import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #ffffff;
}

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── Force ALL markdown text to bright white ── */
.stMarkdown, .stMarkdown p, .stMarkdown li,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4,
.stMarkdown strong, .stMarkdown em,
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li,
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4,
div[data-testid="stMarkdownContainer"] strong,
div[data-testid="stMarkdownContainer"] em,
div[data-testid="stMarkdownContainer"] a {
    color: #ffffff !important;
}

/* ── Hero ── */
.hero { text-align: center; padding: 3.5rem 0 2.5rem; }
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem; font-weight: 500;
    letter-spacing: 0.25em; text-transform: uppercase;
    color: #ff8c32; margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800; line-height: 1.0;
    letter-spacing: -0.03em;
    color: #ffffff; margin: 0 0 1rem;
}
.hero h1 span { color: #ff8c32; }
.hero-sub {
    font-size: 1.05rem; font-weight: 300;
    color: #cccccc; max-width: 520px;
    margin: 0 auto; line-height: 1.65;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
    margin: 2rem 0;
}

.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,140,50,0.15);
    border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 2rem;
}

/* ── Input: white background, black text ── */
.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 2px solid rgba(255,140,50,0.6) !important;
    border-radius: 10px !important;
    color: #000000 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.25) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #888888 !important;
    opacity: 1 !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important;
    font-weight: 500 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #000000 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    opacity: 0.95 !important;
}

/* ── Step cards ── */
.step-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px; padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem; position: relative; overflow: hidden;
}
.step-card.active { border-color: rgba(255,140,50,0.6); background: rgba(255,140,50,0.08); }
.step-card.done   { border-color: rgba(80,200,120,0.5); background: rgba(80,200,120,0.06); }
.step-card::before {
    content:''; position:absolute; left:0; top:0; bottom:0; width:3px;
    border-radius:14px 0 0 14px; background:rgba(255,255,255,0.08);
}
.step-card.active::before { background: #ff8c32; }
.step-card.done::before   { background: #50c878; }

.step-header { display:flex; align-items:center; gap:0.8rem; margin-bottom:0.4rem; }
.step-num    { font-family:'DM Mono',monospace; font-size:0.7rem; color:#ff8c32; font-weight:600; }
.step-title  { font-family:'Syne',sans-serif; font-size:1rem; font-weight:700; color:#ffffff; }
.step-desc   { font-size:0.85rem; color:#bbbbbb; margin-top:0.2rem; }
.step-status { margin-left:auto; font-family:'DM Mono',monospace; font-size:0.7rem; font-weight:600; }
.status-waiting { color: #666666; }
.status-running { color: #ff8c32; }
.status-done    { color: #50c878; }

/* ── Result panels ── */
.result-panel {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px; padding: 1.8rem 2rem;
    margin-top: 1rem; margin-bottom: 1.5rem;
}
.result-panel-title {
    font-family:'DM Mono',monospace; font-size:0.72rem;
    letter-spacing:0.2em; text-transform:uppercase; color:#ff8c32;
    margin-bottom:1rem; padding-bottom:0.7rem;
    border-bottom:1px solid rgba(255,140,50,0.2);
}
.result-content {
    font-size:0.92rem; line-height:1.8;
    color:#ffffff; white-space:pre-wrap;
}

/* ── Report & Feedback panels ── */
.report-panel {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,140,50,0.3);
    border-radius: 16px; padding: 2rem 2.5rem; margin-top: 1rem;
}
.feedback-panel {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(80,200,120,0.3);
    border-radius: 16px; padding: 2rem 2.5rem; margin-top: 1rem;
}
.panel-label {
    font-family:'DM Mono',monospace; font-size:0.72rem;
    letter-spacing:0.2em; text-transform:uppercase;
    margin-bottom:1.2rem; padding-bottom:0.7rem; font-weight:600;
}
.panel-label.orange { color:#ff8c32; border-bottom:1px solid rgba(255,140,50,0.2); }
.panel-label.green  { color:#50c878; border-bottom:1px solid rgba(80,200,120,0.2); }

/* ── Force text inside report and feedback panels to white ── */
.report-panel p, .report-panel li, .report-panel h1,
.report-panel h2, .report-panel h3, .report-panel h4,
.report-panel strong, .report-panel em, .report-panel a,
.feedback-panel p, .feedback-panel li, .feedback-panel h1,
.feedback-panel h2, .feedback-panel h3, .feedback-panel h4,
.feedback-panel strong, .feedback-panel em, .feedback-panel a {
    color: #ffffff !important;
}

.section-heading {
    font-family:'Syne',sans-serif; font-size:1.4rem;
    font-weight:700; color:#ffffff; margin:2rem 0 1rem;
}

.chip {
    display:inline-block;
    background:rgba(255,255,255,0.07);
    border:1px solid rgba(255,255,255,0.12);
    border-radius:6px; padding:0.25rem 0.8rem;
    font-size:0.8rem; color:#cccccc;
    margin-right:0.4rem; margin-top:0.3rem;
}

/* ── Expander ── */
details summary {
    color: #ffffff !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* ── Download button ── */
div[data-testid="stDownloadButton"] button {
    background: rgba(255,255,255,0.08) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    padding: 0.5rem 1.2rem !important;
    width: auto !important;
}
div[data-testid="stDownloadButton"] button:hover {
    background: rgba(255,255,255,0.15) !important;
    border-color: rgba(255,255,255,0.35) !important;
}

/* ── Spinner text ── */
div[data-testid="stSpinner"] p {
    color: #ff8c32 !important;
}

/* ── Warning box ── */
div[data-testid="stAlert"] {
    background: rgba(255,140,50,0.1) !important;
    border: 1px solid rgba(255,140,50,0.3) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
}

.notice {
    font-family:'DM Mono',monospace; font-size:0.72rem;
    color:#555555; text-align:center; margin-top:3rem; letter-spacing:0.08em;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: step card ─────────────────────────────────────────────────────────
def step_card(num, title, state, desc=""):
    status_map = {
        "waiting": ("WAITING",   "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",    "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        <div class="step-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout ────────────────────────────────────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:0.5rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.7rem;color:#666;letter-spacing:0.1em;">TRY →</span>
        <span class="chip">LLM agents 2025</span>
        <span class="chip">CRISPR gene editing</span>
        <span class="chip">Fusion energy progress</span>
    </div>
    """, unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)
    r = st.session_state.results

    def s(step):
        steps = ["search", "reader", "writer", "critic"]
        if step in r: return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent", s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent", s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain", s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain", s("critic"), "Reviews & scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "input": f"Find recent, reliable and detailed information about: {topic_val}"
        })
        results["search"] = sr["output"]
        st.session_state.results = dict(results)

    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "input": (
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )
        })
        results["reader"] = rr["output"]
        st.session_state.results = dict(results)

    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results ───────────────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Search Agent Output</div>'
                f'<div class="result-content">{r["search"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Reader Agent Output</div>'
                f'<div class="result-content">{r["reader"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    if "writer" in r:
        st.markdown(
            '<div class="report-panel">'
            '<div class="panel-label orange">📝 Final Research Report</div>',
            unsafe_allow_html=True
        )
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown(
            '<div class="feedback-panel">'
            '<div class="panel-label green">🧐 Critic Feedback</div>',
            unsafe_allow_html=True
        )
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="notice">ResearchMind · Powered by Groq + LangChain · Built with Streamlit</div>',
    unsafe_allow_html=True
)