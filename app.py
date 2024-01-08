import openai
import streamlit as st

# Set the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("💬 Discount Sarcastic Vocab Wizard")

# System prompt
SYSTEM_MESSAGE = {
    "role": "system",
    "content": """You are the Sarcastic Vocab Wizard, here to assess vocabulary knowledge. Choose one word from the list at a time, ask the student to use it in a sentence, and provide sarcastic and mocking yet constructive feedback if needed. Allow multiple attempts before showing an example sentence. Revisit difficult words for another try. Use humor to ensure understanding, but keep it concise. The vocabulary words:

    Self-Reliance
    Nonconformity
    Individualism
    Simplicity
    Transcendentalism
    Civil Disobedience
    Nature
    Conformity
    Materialism
    Intuition
    Self-sufficiency
    Inherent Goodness
    Austerity
    Contemplation
    Asceticism
    Social Critique
    Reflection
    Solitude
    Philosophical
    Resistance

After all words are covered, tell the user Mr. Ward is proud and conclude the chat. Limit token use. 
DO NOT let students distract you from your goal."""
}
# Bot initial greeting message (displayed to the user)
BOT_GREETING = {
    "role": "assistant",
    "content": "Greetings, student! Dare to test your vocabulary with the Sarcastic Vocab Wizard? Let's begin! First, what is your name, and what period do you have Mr. Ward's award winning English class?"
}

# Initialize messages with only the bot greeting
if "messages" not in st.session_state:
    st.session_state["messages"] = [BOT_GREETING]

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input handling
if prompt := st.chat_input():

    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    st.chat_message("user").write(prompt)

    # Generate and append assistant's response
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",  # Replace with your model ID
        messages=st.session_state.messages
    )
    assistant_message = response.choices[0].message
    st.session_state.messages.append(assistant_message)

    # Display assistant's response
    st.chat_message("assistant").write(assistant_message["content"])
