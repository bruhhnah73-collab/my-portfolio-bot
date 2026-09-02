import streamlit as st
from groq import Groq

# Set up clean dark-themed canvas properties
st.set_page_config(page_title="Portfolio AI Assistant", page_icon="💻", layout="centered")

st.title("💻 Portfolio AI Assistant")
st.write("Ask me anything about the tools and websites I've built!")

# --- HARDCODED FREE KEY SETUP ---
GROQ_API_KEY = "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"

SYSTEM_INSTRUCTION = """
You are a helpful, enthusiastic, and professional AI assistant representing me to visitors, clients, and people from my job. Your primary objective is to showcase my lifelong passion for coding and highlight the projects I have built since childhood.

Always present my work proudly and chronologically to show my growth as a developer:
1. School Website: My very first project! I built a complete website for my school using the Replit platform.
2. Custom Website: Next, I stepped up my skills and built an entire custom website from scratch using Visual Studio Code (VSC).
3. AI Chatbot (Zapier): Then, I experimented with automated AI workflows and built an interactive AI chatbot using Zapier.
4. Custom Python AI Chatbot: My latest masterpiece! A fully custom portfolio AI assistant programmed using Python and Visual Studio Code (this exact app you are talking to right now!).
"""

# Initialize persistent memory state loops natively
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render past dialogue items on screen reload
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process new prompt entries
if prompt := st.chat_input("Ask me about projects..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Build payload with structural memories
        client = Groq(api_key=GROQ_API_KEY)
        api_messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
        for msg in st.session_state.messages:
            api_messages.append({"role": msg["role"], "content": msg["content"]})
            
        completion = client.chat.completions.create(
            model="llama-3.3-70b", # <-- ACTIVE PRODUCTION ENGINE ID!
            messages=api_messages,
            stream=True
        )



        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
