import streamlit as ui
from groq import Groq

# 1. Set up the web page title and icon layout cleanly
ui.set_page_config(page_title="My AI Portfolio Bot", page_icon="💻", layout="centered")

# --- COMPATIBLE PRODUCTION CSS SYSTEM ---
ui.markdown("""
<style>
    /* target human chat block wraps explicitly and push right */
    .st-emotion-cache-janwst {
        flex-direction: row-reverse !important;
    }
    /* alter user chat bubble inner values dynamically */
    .st-emotion-cache-janwst div[data-testid="stMarkdownContainer"] {
        background-color: #0b5ed7 !important;
        color: white !important;
        border-radius: 15px 15px 0px 15px !important;
        padding: 12px 18px !important;
    }
    /* alter assistant chat bubble inner values dynamically */
    .st-emotion-cache-4qi9v6 div[data-testid="stMarkdownContainer"] {
        background-color: #2b2b2b !important;
        color: #f0f2f6 !important;
        border-radius: 15px 15px 15px 0px !important;
        padding: 12px 18px !important;
    }
</style>
""", unsafe_allow_html=True)

ui.title("💻 My AI Portfolio Bot")
ui.write("Welcome to my portfolio! Ask me anything about the websites and tools I have built.")

# --- HARDCODED FREE KEY SETUP ---
GROQ_API_KEY = "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"

# --- CUSTOM PORTFOLIO MEMORY & PERSONALITY ---
SYSTEM_INSTRUCTION = """
You are a helpful, enthusiastic, and professional AI assistant representing me to visitors, clients, and people from my job. Your primary objective is to showcase my lifelong passion for coding and highlight the projects I have built since childhood.

Always present my work proudly and chronologically to show my growth as a developer:
1. School Website: My very first project! I built a complete website for my school using the Replit platform.
2. Custom Website: Next, I stepped up my skills and built an entire custom website from scratch using Visual Studio Code (VSC).
3. AI Chatbot (Zapier): Then, I experimented with automated AI workflows and built an interactive AI chatbot using Zapier.
4. Custom Python AI Chatbot: My latest masterpiece! A fully custom portfolio AI assistant programmed using Python and Visual Studio Code (this exact web app you are talking to right now!).

Be engaging, confident, and explain how I have evolved from a kid tinkering on Replit into a software builder using advanced languages like Python and professional tools like VSC.
"""

# 2. Initialize the chat history inside app memory with the instructions hidden
if "messages" not in ui.session_state:
    ui.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "assistant", "content": "Hello! I am here to tell you all about the incredible websites my creator has built since childhood. What project would you like to hear about first?"}
    ]

# 3. Display previous chat messages on every app refresh
for msg in ui.session_state.messages:
    if msg["role"] != "system":  
        # Match standard alignment blocks cleanly via framework roles
        avatar_icon = "🧑‍💻" if msg["role"] == "user" else "🤖"
        with ui.chat_message(msg["role"], avatar=avatar_icon):
            ui.write(msg["content"])

# 4. Handle new user messages typed into the chat bar
if user_input := ui.chat_input():
    client = Groq(api_key=GROQ_API_KEY)

    # Append user's message to the memory and display it instantly
    ui.session_state.messages.append({"role": "user", "content": user_input})
    with ui.chat_message("user", avatar="🧑‍💻"):
        ui.write(user_input)

    # Use an active, ultra-fast model from Groq
    try:
        response_stream = client.chat.completions.create(
            model="openai/gpt-oss-120b", 
            messages=ui.session_state.messages,
            stream=True
        )
    except Exception:
        response_stream = client.chat.completions.create(
            model="qwen/qwen3.6-27b", 
            messages=ui.session_state.messages,
            stream=True
        )
    
    # --- FIXED STREAM PARSER LOOP ---
    def generate_clean_text(stream):
        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                # Adding [0] fixes the list attribute error entirely!
                if chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

    # Render the text piece by piece beautifully in real-time on left side
    with ui.chat_message("assistant", avatar="🤖"):
        ai_response = ui.write_stream(generate_clean_text(response_stream))
    
    # Append the completed response back to the persistent chat history
    ui.session_state.messages.append({"role": "assistant", "content": ai_response})
