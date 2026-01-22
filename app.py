import streamlit as st
import ollama
import uuid
import re

# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="Scholar AI",
    layout="wide"
)

# ---------------- SESSION ----------------

if "researches" not in st.session_state:
    st.session_state.researches = {}

if "current_id" not in st.session_state:
    st.session_state.current_id = None

if "busy" not in st.session_state:
    st.session_state.busy = False


# ---------------- AUTO CREATE FIRST RESEARCH ----------------

if st.session_state.current_id is None:

    rid = str(uuid.uuid4())

    st.session_state.researches[rid] = {
        "title": "New Research",
        "messages": []
    }

    st.session_state.current_id = rid


# ---------------- CSS ----------------

st.markdown("""
<style>

body {
    background-color: #0c1117;
    color: #e5e7eb;
}

.main {
    background-color: #0c1117;
}

.chatbox {
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 12px;
    font-size: 16px;
    line-height: 1.6;
    color: #e5e7eb;
    word-wrap: break-word;
}

.userbox {
    background-color: #1f2933;
    border-left: 4px solid #38bdf8;
}

.aibox {
    background-color: #020617;
    border-left: 4px solid #22c55e;
}

.aibox h2 {
    color: #38bdf8;
    margin-top: 20px;
}

.aibox h3 {
    color: #22c55e;
    margin-top: 15px;
}

.aibox b {
    color: #facc15;
}

textarea {
    color: #ffffff !important;
    background-color: #111827 !important;
}

input {
    color: #ffffff !important;
    background-color: #111827 !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("Research Panel")

    if st.button("New Research"):

        rid = str(uuid.uuid4())

        st.session_state.researches[rid] = {
            "title": "New Research",
            "messages": []
        }

        st.session_state.current_id = rid

        st.rerun()


    st.divider()

    st.subheader("Your Research")

    for k, v in st.session_state.researches.items():

        if st.button(v["title"], key=k):

            st.session_state.current_id = k

            st.rerun()



# ---------------- TITLE ----------------

st.markdown("""
<h1 style="text-align:center;
color:#2563eb;
font-weight:800;">
Scholar AI — Your Research Pilot
</h1>
""", unsafe_allow_html=True)

st.divider()


# ---------------- PROMPTS ----------------

def research_prompt(q):

    return f"""
Write a very detailed academic research paper on:

{q}

Must include:

Abstract
Introduction
Domain Headings
Analysis
ASCII Flowchart
Markdown Table
Conclusion
References (APA / IEEE style without links)

Rules:
No URLs
No hyperlinks
Formal academic tone
Very detailed
Generate own subheadings
"""


def followup_prompt(q, context):

    return f"""
Context:
{context}

Question:
{q}

Rules:
Answer directly
Use subheadings
Accurate
"""


# ---------------- STREAM ----------------

def stream_ai(prompt):

    stream = ollama.chat(
        model="qwen2.5:3b",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in stream:

        if "message" in chunk:

            yield chunk["message"]["content"]



# ---------------- FORMAT HEADINGS ----------------

def format_text(text):

    # ### -> h3
    text = re.sub(r"### (.*)", r"<h3>\1</h3>", text)

    # ## -> h2
    text = re.sub(r"## (.*)", r"<h2>\1</h2>", text)

    # **bold**
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

    return text



# ---------------- CHAT DISPLAY ----------------

if st.session_state.current_id:

    chat = st.session_state.researches[
        st.session_state.current_id
    ]["messages"]

    for m in chat:

        if m["role"] == "user":

            st.markdown(f"""
<div class="chatbox userbox">
<b>You:</b><br>
{m['content']}
</div>
""", unsafe_allow_html=True)

        else:

            formatted = format_text(m["content"])

            st.markdown(f"""
<div class="chatbox aibox">
<b>Scholar:</b><br>
{formatted}
</div>
""", unsafe_allow_html=True)



# ---------------- INPUT ----------------

st.markdown("<br><br>", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):

    col1, col2 = st.columns([10, 1])

    with col1:

        user_input = st.text_input(
            "Type your research question",
            key="input_box",
            label_visibility="collapsed",
            placeholder="Type your research question..."
        )

    with col2:

        send = st.form_submit_button("↑")



# ---------------- SEND ----------------

if send and user_input.strip():

    prompt = user_input.strip()

    chat = st.session_state.researches[
        st.session_state.current_id
    ]["messages"]


    # Add user message
    chat.append({
        "role": "user",
        "content": prompt
    })


    # Decide prompt type
    if len(chat) == 1:

        ai_prompt = research_prompt(prompt)

        st.session_state.researches[
            st.session_state.current_id
        ]["title"] = prompt[:40] + "..."

    else:

        context = ""

        for m in chat[:-1]:
            if m["role"] == "assistant":
                context += m["content"] + "\n\n"

        ai_prompt = followup_prompt(prompt, context)



    # Generate AI Response
    with st.spinner("Researching..."):

        holder = st.empty()
        final = ""

        for part in stream_ai(ai_prompt):

            final += part

            formatted = format_text(final)

            holder.markdown(f"""
<div class="chatbox aibox">
<b>Scholar:</b><br>
{formatted}
</div>
""", unsafe_allow_html=True)



    # Save AI message
    chat.append({
        "role": "assistant",
        "content": final
    })


    st.rerun()
