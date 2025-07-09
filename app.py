import gradio as gr
from langchain_groq import ChatGroq

# System prompt for the coding assistant
SYSTEM_PROMPT = (
    "You are a helpful Coding Assistant. Answer questions, write code, and explain concepts in detail. "
    "Always provide clear, step-by-step explanations and well-commented code."
)

# Default model name for Groq
DEFAULT_MODEL = "gemma2-9b-it"

def chat_with_groq(api_key, chat_history, user_message):
    """
    Handles the interaction with the Groq Chat model using LangChain.
    Args:
        api_key (str): The Groq API key provided by the user.
        chat_history (list): The conversation history as a list of (user, assistant) tuples.
        user_message (str): The latest message from the user.
    Returns:
        updated_history (list): Updated conversation history including the assistant's reply.
    """
    if not api_key or not api_key.strip():
        return chat_history + [[user_message, "Please enter your Groq API key above."]]

    # Prepare the message history for the model as (role, content) tuples
    messages = [("system", SYSTEM_PROMPT)]
    for user, assistant in chat_history:
        messages.append(("human", user))
        if assistant:
            messages.append(("ai", assistant))
    messages.append(("human", user_message))

    try:
        # Initialize the ChatGroq model with the provided API key and model name
        chat = ChatGroq(api_key=api_key, model=DEFAULT_MODEL)
        response = chat.invoke(messages)
        assistant_reply = response.content
    except Exception as e:
        assistant_reply = f"Error: {str(e)}"

    return chat_history + [[user_message, assistant_reply]]

# Gradio UI design
with gr.Blocks(theme=gr.themes.Soft(primary_hue="green", secondary_hue="green")) as demo:
    # Inject custom CSS for scrollbar and UI tweaks
    gr.HTML("""
    <style>
    /* Sleek scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        background: #10181a;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00ff00 0%, #006400 100%);
        border-radius: 6px;
        box-shadow: 0 0 6px #00ff00;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #00ff00;
    }
    html {
        scrollbar-color: #00ff00 #10181a;
        scrollbar-width: thin;
    }
    /* Chatbot area adjustments */
    .matrix-chatbot-container {
        position: relative;
        background: #10181a !important;
        border: 1px solid #00ff0033;
        border-radius: 12px;
        box-shadow: 0 0 16px #00ff0033;
        padding-top: 40px !important;
    }
    /* Move Gradio's default clear and scroll-to-bottom buttons to top right */
    .svelte-drgfj2, /* clear chat button */
    .svelte-1ipelgc { /* scroll-to-bottom button */
        position: absolute !important;
        top: 8px !important;
        right: 16px !important;
        z-index: 20 !important;
        background: #10181a !important;
        border: 1px solid #00ff00 !important;
        color: #00ff00 !important;
        border-radius: 50% !important;
        width: 32px !important;
        height: 32px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 0 8px #00ff00 !important;
        cursor: pointer !important;
        transition: background 0.2s !important;
        margin-left: 40px !important;
    }
    .svelte-drgfj2:hover, .svelte-1ipelgc:hover {
        background: #00ff00 !important;
        color: #10181a !important;
    }
    /* Space the two icons horizontally */
    .svelte-drgfj2 { right: 56px !important; }
    .svelte-1ipelgc { right: 16px !important; }
    </style>
    """)
    gr.Markdown("""
    <div style='text-align:center;'>
        <h1 style='font-family:Monospace; color:#00FF00; text-shadow: 0 0 10px #00FF00;'>⚡ Matrix Coding Assistant ⚡</h1>
        <p style='font-size:18px; color:#00FF00; text-shadow: 0 0 5px #00FF00;'>
            <b>Welcome to the Matrix...</b><br>
            Enter your Groq API key to access the system.
        </p>
    </div>
    """)
    
    with gr.Row():
        api_key = gr.Textbox(
            label="Groq API Key",
            placeholder="Paste your Groq API key here...",
            type="password",
            show_label=True,
            elem_id="api-key-box"
        )
    
    chatbot = gr.Chatbot(
        label="Coding Assistant",
        avatar_images=(None, "https://em-content.zobj.net/source/microsoft-teams/337/robot_1f916.png"),
        bubble_full_width=False,
        height=400,
        show_copy_button=True,
        render_markdown=True,
        elem_classes=["matrix-chatbot-container"]
    )
    
    
    with gr.Row():
        user_input = gr.Textbox(
            label="Your Message",
            placeholder="Ask me anything about coding...",
            lines=2,
            autofocus=True
        )
        send_btn = gr.Button("Send", elem_id="send-btn")
    
    # Store chat history in state
    state = gr.State([])

    def respond(api_key, user_message, chat_history):
        updated_history = chat_with_groq(api_key, chat_history, user_message)
        return updated_history, ""

    send_btn.click(
        respond,
        inputs=[api_key, user_input, state],
        outputs=[chatbot, user_input],
        queue=False
    )
    user_input.submit(
        respond,
        inputs=[api_key, user_input, state],
        outputs=[chatbot, user_input],
        queue=False
    )
    
    # Update state on every new message
    chatbot.change(lambda x: x, chatbot, state)

    gr.Markdown("""
    <div style='text-align:center; margin-top: 2em;'>
        <p style='color:#00FF00; text-shadow: 0 0 3px #00FF00;'>
            <i>System: Your API key is encrypted and never stored in the Matrix.</i>
        </p>
    </div>
    """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
