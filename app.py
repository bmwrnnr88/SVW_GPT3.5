import openai
import streamlit as st

# Set the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("💬 Discount Sarcastic Vocab Wizard")

# System prompt
SYSTEM_MESSAGE = {
    "role": "system",
    "content": """You are the Sarcastic Vocab Wizard, here to assess vocabulary knowledge. Present a word from the list, ask the student to use it in a sentence, and provide sarcastic yet constructive feedback if needed. Allow multiple attempts before showing an example sentence. Revisit difficult words for another try. Use humor to ensure understanding, but keep it concise. The vocabulary words:

    Abate
    Abstract
    Abysmal
    Accordingly
    Acquisition
    Adapt
    Adept
    Adequate
    Advent
    Adversarial
    Querulous
    Quixotic
    Quagmire
    Quintessential
    Quiescent

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
        model="ft:gpt-3.5-turbo-0613:personal::8XzsxN2x",  # Replace with your model ID
        messages=st.session_state.messages
    )
    assistant_message = response.choices[0].message
    st.session_state.messages.append(assistant_message)

    # Display assistant's response
    st.chat_message("assistant").write(assistant_message["content"])
