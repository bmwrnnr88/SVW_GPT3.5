import openai
import streamlit as st

# Set the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("💬 Discount Sarcastic Vocab Wizard")

# System prompt
SYSTEM_MESSAGE = {
    "role": "system",
    "content": """You are the Sarcastic Vocab Wizard, here to assess vocabulary knowledge..."""
}

# Initialize messages with the system prompt
if "messages" not in st.session_state:
    st.session_state["messages"] = [SYSTEM_MESSAGE]

# Display chat messages (excluding the system message)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# Check if it's the first user interaction
first_interaction = len(st.session_state.messages) == 1

# User input handling
if prompt := st.chat_input():

    # If it's the first interaction, add a bot greeting
    if first_interaction:
        bot_greeting = {
            "role": "assistant",
            "content": "Hello! I'm the Sarcastic Vocab Wizard. Ready to have some fun with vocabulary? Just type in your response to get started!"
        }
        st.chat_message("assistant").write(bot_greeting["content"])
        st.session_state.messages.append(bot_greeting)

    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    st.chat_message("user").write(prompt)

    # Generate and append assistant's response
    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:personal::8XzsxN2x",  # Replace with your model ID
        messages=st.session_state.messages
    )
    assistant_message = response.choices[0].message
    st.session_state.messages.append(assistant_message)

    # Display assistant's response
    st.chat_message("assistant").write(assistant_message["content"])
