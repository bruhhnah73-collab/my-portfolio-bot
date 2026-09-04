import streamlit as st
from groq import Groq

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Portfolio AI Assistant",
    page_icon="💻",
    layout="centered"
)

st.title("💻 Portfolio AI Assistant")
st.write("Ask me anything about the tools and websites I've built!")

# -----------------------------
# Get API key securely
# -----------------------------
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("GROQ_API_KEY is not configured in Streamlit Secrets.")
    st.stop()

# -----------------------------
# AI instructions
# -----------------------------
SYSTEM_INSTRUCTION = """
You are a helpful, enthusiastic, and professional AI assistant
representing me to visitors, clients, and people from my job.

Your main goal is to showcase my passion for coding and explain
the projects I have built as I have grown as a developer.

Present my projects proudly and chronologically:

1. School Website:
My very first project. I built a complete website for my school
using the Replit platform.

2. Custom Website:
I improved my skills and built an entire custom website from
scratch using Visual Studio Code (VSC).

3. AI Chatbot (Zapier):
I experimented with automated AI workflows and built an
interactive AI chatbot using Zapier.

4. Custom Python AI Chatbot:
My latest project. A custom portfolio AI assistant programmed
using Python and Visual Studio Code. This is the application
the visitor is currently using.

Answer questions clearly and naturally.

If someone asks about my projects, explain them using the
information above.

Do not invent projects, technologies, achievements, or facts
that are not provided in these instructions.
"""

# -----------------------------
# Conversation memory
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display previous messages
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat input
# -----------------------------
prompt = st.chat_input("Ask me about my projects...")

if prompt:

    # Display user's message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user's message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Generate assistant response
    with st.chat_message("assistant"):

        message_placeholder = st.empty()
        full_response = ""

        try:
            # Create Groq client
            client = Groq(api_key=GROQ_API_KEY)

            # Build conversation
            api_messages = [
                {
                    "role": "system",
                    "content": SYSTEM_INSTRUCTION
                }
            ]

            for message in st.session_state.messages:
                api_messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })

            # Ask Groq
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=api_messages,
                temperature=0.6,
                max_completion_tokens=1024,
                stream=True,
                include_reasoning=False
            )

            # Stream the response
            for chunk in completion:

                if not chunk.choices:
                    continue

                content = chunk.choices[0].delta.content

                if content:
                    full_response += content

                    message_placeholder.markdown(
                        full_response + "▌"
                    )

            # Final response
            message_placeholder.markdown(full_response)

            # Save response
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

        except Exception as e:
            st.error("Something went wrong while connecting to the AI.")
            st.code(str(e))
