import os
import sqlite3
import time
from datetime import datetime
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

from prompts import CPS_TUTOR_SYSTEM_INSTRUCTION
from secret_retrieval import get_api_key

st.set_page_config(
    page_title="Balu Thatha - CPS Tutor",
    page_icon="👴",
    layout="wide"
)

# --- Path & Persistence Setup ---
DB_DIR = "/data" if os.path.exists("/data") else "."
DB_PATH = os.path.join(DB_DIR, "tutor_data.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

conn = get_db_connection()
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS threads (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id TEXT NOT NULL,
    role TEXT CHECK(role IN ('user', 'model')) NOT NULL,
    content TEXT NOT NULL,
    has_image INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(thread_id) REFERENCES threads(id) ON DELETE CASCADE
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS notebook (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_title TEXT,
    note TEXT NOT NULL,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# --- Secrets & Client Setup ---
api_key = get_api_key()
if not api_key:
    st.error(
        "Missing GEMINI_API_KEY. "
        "Please set it in your Hugging Face Space Settings under Repository Secrets, "
        "or in .streamlit/secrets.toml for local development."
    )
    st.stop()

# Force the real Gemini API endpoint. GOOGLE_GEMINI_BASE_URL may be set
# machine-wide (e.g. pointed at a local model server for unrelated
# projects) — this app should never inherit that.
os.environ["GOOGLE_GEMINI_BASE_URL"] = "https://generativelanguage.googleapis.com"

client = genai.Client(api_key=api_key)

# --- Sidebar: Thread Switcher & Notebook ---
st.sidebar.title("📚 Study Desk")

if st.sidebar.button("➕ New Chat Session", use_container_width=True):
    new_id = f"chat_{int(time.time())}"
    c.execute("INSERT INTO threads (id, title) VALUES (?, ?)", (new_id, "New Session"))
    conn.commit()
    st.session_state.current_thread = new_id
    st.rerun()

threads = c.execute("SELECT id, title FROM threads ORDER BY created_at DESC").fetchall()

if not threads:
    default_id = f"chat_{int(time.time())}"
    c.execute("INSERT INTO threads (id, title) VALUES (?, ?)", (default_id, "First Session"))
    conn.commit()
    threads = [(default_id, "First Session")]

thread_dict = {t[0]: t[1] for t in threads}
if "current_thread" not in st.session_state or st.session_state.current_thread not in thread_dict:
    st.session_state.current_thread = threads[0][0]

selected_thread = st.sidebar.radio(
    "Past Sessions:",
    options=[t[0] for t in threads],
    format_func=lambda tid: thread_dict[tid],
    index=[t[0] for t in threads].index(st.session_state.current_thread)
)
st.session_state.current_thread = selected_thread

# Sidebar Review Notebook
st.sidebar.markdown("---")
st.sidebar.subheader("⭐ Study Notebook")
saved_notes = c.execute(
    "SELECT id, thread_title, note, saved_at FROM notebook ORDER BY saved_at DESC"
).fetchall()

if saved_notes:
    for nid, t_title, note, saved_at in saved_notes[:10]:
        with st.sidebar.expander(f"{t_title[:18]}... ({saved_at[:10]})"):
            st.markdown(note)
            if st.button("Remove", key=f"del_{nid}"):
                c.execute("DELETE FROM notebook WHERE id = ?", (nid,))
                conn.commit()
                st.rerun()
else:
    st.sidebar.caption("No notes saved yet. Click 'Save to Notebook' below any tutor explanation to review later.")

# --- Main Chat Window ---
st.title("👴 Balu Thatha - CPS 7th Grade Academic & Test Prep Tutor")

db_msgs = c.execute(
    "SELECT role, content FROM messages WHERE thread_id = ? ORDER BY created_at ASC",
    (st.session_state.current_thread,)
).fetchall()

for role, content in db_msgs:
    with st.chat_message(role):
        st.markdown(content)

# File Uploader for Homework / Diagnostic Reports
with st.expander("📎 Attach Homework Photo or i-Ready Diagnostic Report"):
    uploaded_file = st.file_uploader("Upload an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    image_preview = None
    if uploaded_file:
        image_preview = Image.open(uploaded_file)
        st.image(image_preview, caption="Attached Homework / Problem", width=320)

# Input Box
if prompt := st.chat_input("Ask a question, paste homework, or request practice..."):
    with st.chat_message("user"):
        if image_preview:
            st.image(image_preview, width=260)
        st.markdown(prompt)

    # Persist user message
    c.execute(
        "INSERT INTO messages (thread_id, role, content, has_image) VALUES (?, ?, ?, ?)",
        (st.session_state.current_thread, "user", prompt, 1 if image_preview else 0)
    )
    conn.commit()

    # Reconstruct multi-turn conversation history for Gemini API
    history_contents = []
    for r, text in db_msgs:
        history_contents.append(
            types.Content(
                role="user" if r == "user" else "model",
                parts=[types.Part.from_text(text=text)]
            )
        )

    current_parts = []
    if image_preview and uploaded_file:
        current_parts.append(
            types.Part.from_bytes(
                data=uploaded_file.getvalue(),
                mime_type=uploaded_file.type or "image/png",
            )
        )
    current_parts.append(types.Part.from_text(text=prompt))
    history_contents.append(types.Content(role="user", parts=current_parts))

    # Generate model response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=history_contents,
                config=types.GenerateContentConfig(
                    system_instruction=CPS_TUTOR_SYSTEM_INSTRUCTION,
                    temperature=0.4,
                )
            )
            reply_text = response.text
            st.markdown(reply_text)

    # Persist model message
    c.execute(
        "INSERT INTO messages (thread_id, role, content) VALUES (?, ?, ?)",
        (st.session_state.current_thread, "model", reply_text)
    )

    # Auto-title thread on first message
    if len(db_msgs) == 0:
        clean_title = prompt[:26] + "..." if len(prompt) > 26 else prompt
        c.execute(
            "UPDATE threads SET title = ? WHERE id = ?",
            (clean_title, st.session_state.current_thread)
        )

    conn.commit()
    st.rerun()

# --- Notebook Quick-Save Button ---
if db_msgs:
    last_model_msg = next((content for role, content in reversed(db_msgs) if role == "model"), None)
    if last_model_msg:
        if st.button("⭐ Save Last Tutor Explanation to Study Notebook"):
            active_title = thread_dict.get(st.session_state.current_thread, "Tutoring Note")
            c.execute(
                "INSERT INTO notebook (thread_title, note) VALUES (?, ?)",
                (active_title, last_model_msg)
            )
            conn.commit()
            st.toast("Saved to your study notebook! 📓")
            st.rerun()