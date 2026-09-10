import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

from agents.data_agent import data_agent

st.set_page_config(page_title="AI Data Agent", page_icon="🤖", layout="centered")

# ---------------------------------------------------------------------------
# Custom styling — dark background, mint-green accent, monospace tag font
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@400;600;800&display=swap');

    :root {
        --bg: #0a0f0d;
        --accent: #34d399;
        --accent-dim: #1f7a5c;
        --muted: #8b98a5;
        --border: #1f2b27;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg);
        color: #e5e7eb;
    }

    .stApp {
        background: radial-gradient(circle at 20% 0%, #10201a 0%, #0a0f0d 55%);
    }

    /* Hide default streamlit chrome */
    #MainMenu, header, footer {visibility: hidden;}

    /* Brand tag */
    .brand {
        font-family: 'JetBrains Mono', monospace;
        color: var(--accent);
        font-size: 1.1rem;
        letter-spacing: 1px;
        margin-bottom: 0.2rem;
    }
    .brand span { color: #e5e7eb; }

    .tagline {
        font-family: 'JetBrains Mono', monospace;
        color: var(--muted);
        font-size: 0.8rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }

    h1.title {
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0 0 0.3rem 0;
        color: #f3f4f6;
    }

    p.subtitle {
        color: var(--accent);
        font-size: 1.15rem;
        margin-bottom: 0.6rem;
    }

    p.description {
        color: var(--muted);
        font-size: 0.95rem;
        max-width: 640px;
        line-height: 1.5;
    }

    hr.divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 1.5rem 0;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: #121a17 !important;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.4rem 0.6rem;
    }

    /* Chat input box */
    [data-testid="stChatInput"] textarea {
        background-color: #0f1512 !important;
        color: #e5e7eb !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
    }

    /* Buttons (if any) */
    .stButton>button {
        background-color: var(--accent);
        color: #06251b;
        font-weight: 700;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: var(--accent-dim);
        color: white;
    }

    /* Stats row */
    .stats {
        display: flex;
        gap: 3rem;
        margin-top: 1rem;
    }
    .stat-num {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--accent);
        font-family: 'JetBrains Mono', monospace;
    }
    .stat-label {
        color: var(--muted);
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown('<div class="brand">agent<span>.chat</span> _</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">SQL + ETL &nbsp;/&nbsp; LangGraph &nbsp;/&nbsp; OpenAI</div>', unsafe_allow_html=True)
st.markdown('<h1 class="title">AI Data Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ask anything about your data</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="description">Natural language in, structured answers out — routes your '
    'question to a SQL analyst or an ETL agent depending on what you\'re asking for.</p>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Chat state
# ---------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []


def extract_final_answer(result: dict) -> str:
    route = result.get("route_response")
    last = result["messages"][-1]

    if route == "etl" and isinstance(last, dict):
        sub_messages = last.get("messages", [])
        if sub_messages:
            content = getattr(sub_messages[-1], "content", None)
            if content:
                return content
        return str(last)

    if route == "sql" and isinstance(last, dict):
        if last.get("final_answer"):
            return last["final_answer"]
        return str(last)

    content = getattr(last, "content", None)
    return content if content else str(last)


for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask your question...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = data_agent.invoke({
                    "messages": [HumanMessage(content=user_input)],
                    "route_response": ""
                })
                answer = extract_final_answer(result)
            except Exception as e:
                answer = f"⚠️ Something went wrong: {e}"
            st.markdown(answer)

    st.session_state.history.append({"role": "assistant", "content": answer})