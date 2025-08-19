import streamlit as st
import time
from utils.config import get_env
from models.chat_models import ChatModel

st.set_page_config(
    page_title="COLLAR AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
  :root {
    --bg: #0f1115;
    --panel: #15181e;
    --panel-2: #1b1f27;
    --border: #262a31;
    --text: #e5e7eb;
    --muted: #a1a7b3;
    --accent: #6b7280;
  }
  .stApp { background: var(--bg); }
  .block-container { padding-top: 1rem; padding-bottom: 6rem; }

  .cb-header { text-align: center; margin: 0 0 1rem 0; }
  .cb-title { color: var(--text); font-size: 2.6rem; font-weight: 800; letter-spacing: 0.18em; text-transform: uppercase; margin: 0; }
  .cb-rule { height: 1px; background: var(--border); border: 0; margin: .75rem auto 1.2rem; max-width: 1100px; }

  section[data-testid="stSidebar"] { background: var(--panel); border-right: 1px solid var(--border); }
  .cb-side-h { color: var(--text) !important; font-weight: 700; margin: .6rem 0 .35rem; }
  .cb-chatlist-item { display:flex; align-items:center; gap:.35rem; }
  .cb-chat-btn > button { width: 100%; text-align: left; background: var(--panel-2); border:1px solid var(--border); color: var(--text); padding:.3rem .55rem; border-radius: 8px; }
  .cb-chat-del > button { width:100%; background:transparent; color: #ef4444; border:1px solid var(--border); padding:.3rem .4rem; border-radius:8px; }
  .cb-chat-btn > button:hover { filter:brightness(1.05); }

  .cb-chat { max-width: 1100px; margin: 0 auto; }
  .thinking { display: inline-flex; align-items: center; gap: .35rem; color: var(--muted); }
  .thinking-dot { width: 6px; height: 6px; background: var(--accent); border-radius: 50%; opacity: .6; animation: pulse 1.4s infinite ease-in-out; }
  .thinking-dot:nth-child(2){ animation-delay: .18s; }
  .thinking-dot:nth-child(3){ animation-delay: .36s; }
  @keyframes pulse { 0%,100%{ transform: scale(1); opacity:.4 } 50%{ transform: scale(1.25); opacity:1 } }

  .cb-input-wrap { position: fixed; left: 50%; transform: translateX(-50%); bottom: 14px; width: 60%; max-width: 720px; z-index: 100; }
  .cb-input { background: var(--panel-2); border: 1px solid var(--border); border-radius: 12px; padding: .25rem .5rem; display: flex; gap: .5rem; align-items: center; }
  .cb-input .stTextInput input { background: transparent !important; color: var(--text) !important; border: none !important; box-shadow: none !important; }
  .cb-input .stTextInput div div { border: none !important; }
  .cb-input .stButton>button { background: var(--accent); color: #fff; border: none; padding: .4rem .9rem; border-radius: 10px; font-weight: 600; }
  .cb-input .stButton>button:hover { filter: brightness(1.1); }

  .cb-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.55); z-index: 200; }
  .cb-modal { position: fixed; inset: 0; display: grid; place-items: center; z-index: 201; }
  .cb-modal-card { background: var(--panel-2); border: 1px solid var(--border); border-radius: 10px; padding: 1rem; width: 92%; max-width: 560px; color: var(--text); }
  .cb-modal-h { font-size: 1.1rem; font-weight: 700; margin: 0 0 .5rem; display:flex; align-items:center; justify-content:space-between; }
  .cb-x > button { background: transparent; color: var(--muted); border: 1px solid var(--border); padding: .2rem .5rem; border-radius: 8px; }
  .cb-kv { display: flex; justify-content: space-between; gap: 1rem; padding: .5rem 0; border-bottom: 1px solid var(--border); }
  .cb-kv:last-child { border-bottom: 0; }
  .cb-badge { display:inline-flex; align-items:center; gap:.4rem; font-size:.85rem; color: var(--muted); }
  .cb-dot { width: 8px; height: 8px; border-radius: 50%; background: #6b7280; }
  .cb-dot.ok { background: #22c55e; }
  .cb-dot.err { background: #ef4444; }

  #MainMenu, header { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
<div class="cb-header">
  <h1 class="cb-title">COLLAR AI</h1>
  <hr class="cb-rule" />
</div>
""",
    unsafe_allow_html=True,
)

# Session state bootstrapping
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "show_api_modal" not in st.session_state:
    st.session_state.show_api_modal = False
if "cb_input" not in st.session_state:
    st.session_state.cb_input = ""
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False
if "stop_generation" not in st.session_state:
    st.session_state.stop_generation = False
if "editing_message" not in st.session_state:
    st.session_state.editing_message = None

# Helpers
def new_chat() -> str:
    chat_id = str(int(time.time() * 1000))
    st.session_state.chats[chat_id] = {
        "title": "New chat",
        "created": time.time(),
        "updated": time.time(),
        "messages": [],
    }
    st.session_state.current_chat_id = chat_id
    return chat_id

def current_messages():
    cid = st.session_state.current_chat_id
    if not cid or cid not in st.session_state.chats:
        cid = new_chat()
    return st.session_state.chats[cid]["messages"], cid

# Sidebar
with st.sidebar:
    st.markdown("<div class='cb-side-h'>Chats</div>", unsafe_allow_html=True)
    if st.button("+ New Chat", use_container_width=True):
        new_chat()
        st.rerun()

    # Chat list (most recent first)
    if st.session_state.chats:
        items = sorted(
            st.session_state.chats.items(), key=lambda kv: kv[1]["updated"], reverse=True
        )
        for chat_id, meta in items:
            c1, c2 = st.columns([6, 1])
            with c1:
                if st.button(meta.get("title", "Chat"), key=f"chat_{chat_id}", use_container_width=True):
                    st.session_state.current_chat_id = chat_id
                    st.rerun()
            with c2:
                if st.button("🗑️", key=f"del_{chat_id}"):
                    try:
                        del st.session_state.chats[chat_id]
                    except KeyError:
                        pass
                    if not st.session_state.chats:
                        new_chat()
                    else:
                        st.session_state.current_chat_id = next(iter(st.session_state.chats.keys()))
                    st.rerun()

    st.markdown("<div class='cb-side-h'>Configuration</div>", unsafe_allow_html=True)
    model_name = st.selectbox("Choose AI Model", ["llama3", "mistral", "llama2", "codellama"], help="Select the AI model to use")
    use_live_data = st.checkbox("Use Live Web + Social Data", value=True, help="Enable real-time web + social data")

    st.markdown("<div class='cb-side-h'>Image Generation</div>", unsafe_allow_html=True)
    image_api = st.selectbox("Image API", ["stability", "bria", "auto"], help="Choose the image generation API")

    st.markdown("<div class='cb-side-h'>API</div>", unsafe_allow_html=True)
    if st.button("API STATUS", use_container_width=True):
        st.session_state.show_api_modal = not st.session_state.show_api_modal
        st.rerun()

    st.markdown("<div class='cb-side-h'>Ollama</div>", unsafe_allow_html=True)
    try:
        _ = ChatModel()
        st.caption("Ollama: Connected")
    except Exception as e:
        st.caption(f"Ollama: Not Connected ({e})")

# API status modal
if st.session_state.show_api_modal:
    apis_to_check = {
        "SERP API": "SERP_API_KEY",
        "Reddit": "REDDIT_CLIENT_ID",
        "Twitter": "TWITTER_BEARER_TOKEN",
        "Stability AI": "STABILITY_API_KEY",
        "Bria AI": "BRIA_API_KEY",
    }
    statuses = {name: bool(get_env(var)) for name, var in apis_to_check.items()}

    st.markdown("<div class='cb-overlay'></div>", unsafe_allow_html=True)
    st.markdown("<div class='cb-modal'>", unsafe_allow_html=True)
    st.markdown("<div class='cb-modal-card'>", unsafe_allow_html=True)
    xcol1, xcol2 = st.columns([10, 1])
    with xcol1:
        st.markdown("<div class='cb-modal-h'>API Status</div>", unsafe_allow_html=True)
    with xcol2:
        if st.button("✕", key="api_close_x"):
            st.session_state.show_api_modal = False
            st.rerun()

    for name, ok in statuses.items():
        dot_class = "ok" if ok else "err"
        status = "Configured" if ok else "Missing"
        st.markdown(
            f"<div class='cb-kv'><span>{name}</span><span class='cb-badge'><span class='cb-dot {dot_class}'></span>{status}</span></div>",
            unsafe_allow_html=True,
        )
    if st.button("Close", key="api_close_btn", use_container_width=True):
        st.session_state.show_api_modal = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Chat history for current chat
messages, current_id = current_messages()

st.markdown("<div class='cb-chat'>", unsafe_allow_html=True)
for i, message in enumerate(messages):
    with st.chat_message(message["role"]):
        # Add edit button for user messages
        if message["role"] == "user":
            col1, col2 = st.columns([20, 1])
            with col1:
                st.markdown(message["content"])
            with col2:
                if st.button("✏️", key=f"edit_{i}", help="Edit this message"):
                    st.session_state.editing_message = i
                    st.session_state.cb_input = message["content"]
                    st.rerun()
        else:
            st.markdown(message["content"])

# Send handler via callback
def on_send():
    text = st.session_state.cb_input.strip()
    if not text:
        return
    st.session_state.to_send = text
    st.session_state.cb_input = ""
    st.session_state.is_generating = True
    st.session_state.stop_generation = False

def on_stop():
    st.session_state.stop_generation = True
    st.session_state.is_generating = False

# Compact input bar
st.markdown("<div class='cb-input-wrap'><div class='cb-input'>", unsafe_allow_html=True)
col_in, col_btn = st.columns([6, 1])
with col_in:
    # Show different placeholder when editing
    placeholder = "Edit message..." if st.session_state.editing_message is not None else "Ask me anything..."
    st.text_input(
    "Prompt",  # Non-empty label for accessibility
    placeholder=placeholder,
    key="cb_input",
    label_visibility="collapsed"
)
with col_btn:
    if st.session_state.is_generating:
        if st.button("⏹️ Stop", use_container_width=True, on_click=on_stop):
            pass
    else:
        button_text = "Update" if st.session_state.editing_message is not None else "Send"
        st.button(button_text, use_container_width=True, on_click=on_send)
st.markdown("</div></div>", unsafe_allow_html=True)

# Handle send deferred from callback
if st.session_state.get("to_send"):
    msg = st.session_state.to_send
    del st.session_state["to_send"]
    
    # Handle editing existing message
    if st.session_state.editing_message is not None:
        edit_index = st.session_state.editing_message
        if edit_index < len(messages):
            # Replace the message at edit_index
            messages[edit_index] = {"role": "user", "content": msg}
            # Remove all messages after the edited message
            messages[:] = messages[:edit_index + 1]
        st.session_state.editing_message = None
    else:
        # Add new message
        messages.append({"role": "user", "content": msg})
    
    chat_meta = st.session_state.chats[current_id]
    if chat_meta.get("title", "New chat") == "New chat":
        chat_meta["title"] = (msg[:40] + ("…" if len(msg) > 40 else ""))
    chat_meta["updated"] = time.time()
    messages.append({"role": "assistant", "content": ""})
    st.rerun()

# If last message is user -> stream assistant
if messages and messages[-1]["role"] == "assistant" and messages[-1]["content"] == "":
    last_user = None
    for m in reversed(messages[:-1]):
        if m["role"] == "user":
            last_user = m["content"]
            break
    if last_user:
        try:
            chat_model = ChatModel()
            full = ""
            with st.chat_message("assistant"):
                ph = st.empty()
                st.markdown("<div class='thinking'><div class='thinking-dot'></div><div class='thinking-dot'></div><div class='thinking-dot'></div></div>", unsafe_allow_html=True)
                for chunk in chat_model.generate_response_stream(model_name, last_user, use_live_data=use_live_data):
                    if st.session_state.stop_generation:
                        full += "\n\n[Generation stopped by user]"
                        break
                    full += chunk
                    ph.markdown(full + "▌")
                ph.markdown(full)
            messages[-1] = {"role": "assistant", "content": full}
            st.session_state.chats[current_id]["updated"] = time.time()
        except Exception as e:
            err = f"❌ Error: {e}"
            with st.chat_message("assistant"):
                st.markdown(err)
            messages[-1] = {"role": "assistant", "content": err}
            st.session_state.chats[current_id]["updated"] = time.time()
        finally:
            # Reset generation states
            st.session_state.is_generating = False
            st.session_state.stop_generation = False

st.markdown("</div>", unsafe_allow_html=True)
