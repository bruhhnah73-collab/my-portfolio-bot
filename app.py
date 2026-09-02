import gradio as gr
from groq import Groq

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

def chat_function(message, history):
    client = Groq(api_key=GROQ_API_KEY)
    
    # Formulate messages array with the hidden system instructions
    messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for user_msg, ai_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": ai_msg})
    messages.append({"role": "user", "content": message})
    
    # Request a sub-second response stream from Groq
    response_stream = client.chat.completions.create(
        model="llama-3.3-70b-specdec", 
        messages=messages,
        stream=True
    )
    
    partial_text = ""
    for chunk in response_stream:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            partial_text += chunk.choices[0].delta.content
            yield partial_text

# Custom theme colors to perfectly match your dark portfolio layout
custom_theme = gr.themes.Default(
    primary_hue="blue",
    neutral_hue="slate"
).set(
    body_background_fill="#1a1a1a",
    body_text_color="#f8fafc",
    block_background_fill="#2b2b2b"
)

with gr.Blocks(theme=custom_theme, title="Portfolio AI Assistant") as demo:
    gr.Markdown("### 💻 Portfolio AI Assistant\nAsk me anything about the websites I've built!")
    gr.ChatInterface(
        fn=chat_function,
        type="messages"
    )

demo.queue().launch(share=False)
