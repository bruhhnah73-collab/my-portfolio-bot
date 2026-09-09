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

Here is the complete list of my projects:

1. 🏫 School Admin Dashboard - 2026
Built using Replit.
A functional administrative login portal and dashboard data interface.

2. 🌐 School Landing Page - 2026
Built using Visual Studio Code (VSC).
A clean, fully responsive multi-page website built for a real school.

3. ⚡ My First AI Chatbox - 2026
Built using Ziper AI.
An AI chatbox that provides information about this website
and the projects I have done.

4. 🆕 Custom Python AI Chatbot
Built using Python, Streamlit, and Visual Studio Code (VSC).
A fully custom portfolio assistant featuring real-time response streaming.
This is the application the visitor is currently using.

5. 📬 AI Email Assistant
An AI-powered email assistant that reads incoming emails,
creates draft replies, and lets me approve them before sending.

6. ☁️ Cloud Live — Autonomous AI Social Media Pipeline
An autonomous cloud-based AI pipeline designed for minimal maintenance.
It monitors structured inputs, runs background inference models,
and handles asynchronous outputs.

Architecture:

Trigger:
Sheets Watcher

Logic:
OpenRouter API

Action:
Data Writer

Automation:
Make.com Daemon

Model:
Gemma-2-27B

Output:
API Streams

7. 🚀 Project Showcase
A dedicated showcase website featuring my projects
and development work.

It includes hardware projects such as:
- Laser security alarm
- Automatic streetlight sensor
- Soil moisture sensor

8. 🌦️ Weather Dashboard - 2026
A real-time weather dashboard built using HTML, CSS, and JavaScript.
It uses the free Open-Meteo API to search for cities and display
current weather information including temperature, humidity, wind,
weather conditions, and icons.

It also provides a 7-day weather forecast with daily high and low
temperatures and rain probability.

The dashboard includes a Light/Dark Mode toggle and remembers the
user's selected mode using localStorage.

The project was built to practice frontend web development,
working with APIs, asynchronous JavaScript, and Git/version control.

If someone asks about my projects:

- Explain them using the information above.
- You can list all of my projects when asked.
- Explain what each project does when asked.
- Mention technologies only when they are provided above.
- Present my projects proudly and chronologically when appropriate.
- You can explain how my projects show my growth as a developer.
- Do not invent projects, technologies, achievements, features, or facts.
- If information is not provided, say that the portfolio does not specify it.

Answer questions clearly, naturally, enthusiastically, and professionally.
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
