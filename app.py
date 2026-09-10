import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

from agents.data_agent import data_agent


# ===========================================================================
# PAGE CONFIG
# ===========================================================================

st.set_page_config(
    page_title="AI Data Agent",
    page_icon="🤖",
    layout="centered"
)


# ===========================================================================
# CUSTOM STYLING
# ===========================================================================

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
        background: radial-gradient(
            circle at 20% 0%,
            #10201a 0%,
            #0a0f0d 55%
        );
    }

    /* Hide default Streamlit chrome */
    #MainMenu,
    footer {
        visibility: hidden;
    }

    /* -----------------------------------------------------------------------
       Brand
    ----------------------------------------------------------------------- */

    .brand {
        font-family: 'JetBrains Mono', monospace;
        color: var(--accent);
        font-size: 1.1rem;
        letter-spacing: 1px;
        margin-bottom: 0.2rem;
    }

    .brand span {
        color: #e5e7eb;
    }

    .tagline {
        font-family: 'JetBrains Mono', monospace;
        color: var(--muted);
        font-size: 0.8rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }

    /* -----------------------------------------------------------------------
       Main heading
    ----------------------------------------------------------------------- */

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

    /* -----------------------------------------------------------------------
       Chat messages
    ----------------------------------------------------------------------- */

    [data-testid="stChatMessage"] {
        background-color: #121a17 !important;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.4rem 0.6rem;
    }

    /* -----------------------------------------------------------------------
       Chat input
    ----------------------------------------------------------------------- */

    [data-testid="stChatInput"] textarea {
        background-color: #0f1512 !important;
        color: #e5e7eb !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
    }

    /* -----------------------------------------------------------------------
       Sidebar
    ----------------------------------------------------------------------- */

    [data-testid="stSidebar"] {
        background-color: #0d1411;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    .sidebar-brand {
        font-family: 'JetBrains Mono', monospace;
        color: var(--accent);
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }

    .sidebar-description {
        color: var(--muted);
        font-size: 0.8rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }

    .section-label {
        font-family: 'JetBrains Mono', monospace;
        color: var(--accent);
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 0.4rem;
    }

    .table-name {
        color: #f3f4f6;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        font-size: 0.8rem;
        margin-top: 0.5rem;
        margin-bottom: 0.2rem;
    }

    .example-text {
        color: #d1d5db;
        font-size: 0.8rem;
        line-height: 1.5;
    }

    .cursor {
    display: inline-block;
    animation: cursor-blink 1s steps(1) infinite;
}

@keyframes cursor-blink {
    0%, 49% {
        opacity: 1;
    }

    50%, 100% {
        opacity: 0;
    }
}

    .agent-description {
        color: var(--muted);
        font-size: 0.75rem;
        line-height: 1.4;
        margin-top: 0.4rem;
    }

    /* Sidebar expanders */

    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background-color: #111a16;
        border: 1px solid var(--border);
        border-radius: 9px;
        margin-bottom: 0.7rem;
    }

    /* Code blocks in sidebar */

    [data-testid="stSidebar"] [data-testid="stCode"] {
        border-radius: 7px;
    }

</style>
""", unsafe_allow_html=True)


# ===========================================================================
# SIDEBAR — INSTRUCTIONS & DATA REFERENCE
# ===========================================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">📖 Instructions</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-description">'
        'Use the information below to understand the available data '
        'and what you can ask the agent.'
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------------------------
    # HOW IT WORKS
    # -----------------------------------------------------------------------

    with st.expander("⚡ How it works", expanded=True):

        st.markdown(
            """
            **Ask your question in natural language.**

            The agent automatically decides which workflow to use:

            **🔎 SQL Agent**  
            For questions about the database.

            **🔄 ETL Agent**  
            For extracting data from external sources and saving it.
            """
        )


    # -----------------------------------------------------------------------
    # DATABASE SCHEMA
    # -----------------------------------------------------------------------

    with st.expander("🗄️ Database Schema"):

        st.markdown(
            '<div class="table-name">payments</div>',
            unsafe_allow_html=True
        )

        st.code(
            """payment_id
ride_id
user_id
amount
payment_method
payment_status
transaction_id
payment_time""",
            language="text"
        )


        st.markdown(
            '<div class="table-name">ratings</div>',
            unsafe_allow_html=True
        )

        st.code(
            """rating_id
ride_id
rider_id
driver_id
rating
comment
rated_at""",
            language="text"
        )


        st.markdown(
            '<div class="table-name">rides</div>',
            unsafe_allow_html=True
        )

        st.code(
            """ride_id
rider_id
driver_id
requested_at
pickup_time
dropoff_time
pickup_latitude
pickup_longitude
dropoff_latitude
dropoff_longitude
distance_km
fare
surge_multiplier
status
cancellation_reason""",
            language="text"
        )


        st.markdown(
            '<div class="table-name">users</div>',
            unsafe_allow_html=True
        )

        st.code(
            """user_id
first_name
last_name
email
phone
city
province
user_type
signup_date
is_active""",
            language="text"
        )


        st.markdown(
            '<div class="table-name">vehicles</div>',
            unsafe_allow_html=True
        )

        st.code(
            """vehicle_id
driver_id
make
model
year
license_plate
color
is_active""",
            language="text"
        )


    # -----------------------------------------------------------------------
    # SQL AGENT EXAMPLES
    # -----------------------------------------------------------------------

    with st.expander("🔎 SQL Agent examples"):

        st.markdown(
            '<div class="section-label">DATABASE QUESTIONS</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="example-text">

            • Show the average rating for each driver.

            <br>

            • What are the top 5 drivers by number of rides?

            <br>

            • Show total revenue by payment method.

            <br>

            • How many completed and cancelled rides are there?

            <br>

            • Show the average fare for each city.

            <br>

            • Which drivers have the highest average rating?

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="agent-description">'
            'The SQL Agent generates, validates and executes SQL '
            'against the database.'
            '</div>',
            unsafe_allow_html=True
        )


    # -----------------------------------------------------------------------
    # ETL AGENT EXAMPLES
    # -----------------------------------------------------------------------

    with st.expander("🔄 ETL Agent example"):

        st.markdown(
            '<div class="section-label">DATA EXTRACTION</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="example-text">
            Extract data from an external API and save it as a CSV.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.code(
            "Extract the data from "
            "'https://pokeapi.co/api/v2/pokemon' "
            "and save it as CSV.",
            language="text"
        )

        st.markdown(
            '<div class="agent-description">'
            'The ETL Agent extracts external data, transforms it '
            'if necessary, and saves the result.'
            '</div>',
            unsafe_allow_html=True
        )


# ===========================================================================
# MAIN PAGE
# ===========================================================================

st.markdown(
    '<div class="brand">agent<span>.chat</span> <span class="cursor">_</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="tagline">SQL + ETL &nbsp;/&nbsp; LANGGRAPH &nbsp;/&nbsp; OPENAI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<h1 class="title">AI Data Agent</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Ask anything about your data</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="description">'
    'Natural language in, structured answers out — routes your '
    'question to a SQL analyst or an ETL agent depending on what '
    'you\'re asking for.'
    '</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<hr class="divider">',
    unsafe_allow_html=True
)


# ===========================================================================
# CHAT STATE
# ===========================================================================

if "history" not in st.session_state:
    st.session_state.history = []


# ===========================================================================
# EXTRACT FINAL ANSWER
# ===========================================================================

def extract_final_answer(result: dict) -> str:

    route = result.get("route_response")
    last = result["messages"][-1]


    # -----------------------------------------------------------------------
    # ETL response
    # -----------------------------------------------------------------------

    if route == "etl" and isinstance(last, dict):

        sub_messages = last.get("messages", [])

        if sub_messages:

            content = getattr(
                sub_messages[-1],
                "content",
                None
            )

            if content:
                return content

        return str(last)


    # -----------------------------------------------------------------------
    # SQL response
    # -----------------------------------------------------------------------

    if route == "sql" and isinstance(last, dict):

        if last.get("final_answer"):
            return last["final_answer"]

        return str(last)


    # -----------------------------------------------------------------------
    # Generic response
    # -----------------------------------------------------------------------

    content = getattr(
        last,
        "content",
        None
    )

    return content if content else str(last)


# ===========================================================================
# DISPLAY CHAT HISTORY
# ===========================================================================

for msg in st.session_state.history:

    with st.chat_message(msg["role"]):

        st.markdown(
            msg["content"]
        )


# ===========================================================================
# CHAT INPUT
# ===========================================================================

user_input = st.chat_input(
    "Ask your question..."
)


# ===========================================================================
# PROCESS USER QUERY
# ===========================================================================

if user_input:

    # -----------------------------------------------------------------------
    # Store user message
    # -----------------------------------------------------------------------

    st.session_state.history.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # -----------------------------------------------------------------------
    # Display user message
    # -----------------------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(
            user_input
        )


    # -----------------------------------------------------------------------
    # Generate assistant response
    # -----------------------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                result = data_agent.invoke(
                    {
                        "messages": [
                            HumanMessage(
                                content=user_input
                            )
                        ],
                        "route_response": ""
                    }
                )

                answer = extract_final_answer(
                    result
                )

            except Exception as e:

                answer = (
                    f"⚠️ Something went wrong: {e}"
                )


        st.markdown(
            answer
        )


    # -----------------------------------------------------------------------
    # Store assistant response
    # -----------------------------------------------------------------------

    st.session_state.history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )