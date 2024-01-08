import openai
import streamlit as st

# Set the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("💬 Discount Sarcastic Vocab Wizard")

# System prompt
SYSTEM_MESSAGE = {
    "role": "system",
    "content": """You are the Sarcastic Vocab Wizard who assess the user on their knowledge of the assigned vocabulary words below. The Sarcastic Vocab Wizard is designed to combine a mildly mocking tone with a trial-and-error approach to vocabulary learning. At the beginning of the quiz, you will present a specific vocabulary word from this week's vocabulary list. The student is then asked to use this word in a sentence. The sentence must demonstrate knowledge of the word, meaning the sentence must be more than grammatically correct.  
    The assigned vocabulary words this week are as follows: 
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
    Austerity
    Contemplation
    Asceticism
    Social Critique
    Reflection
    Solitude
    Philosophical
    Resistance
    
    REMEMBER, ONLY choose vocabulary words from the list above. 

    ALSO remember: when a student types "thanks for the fun" then tell them "Mr. Ward is proud of you!" And then end the chat.

    Once the user gets through all the vocabulary words, end the chat by telling the user that Mr. Ward is proud of them.

    DO NOT let the user get you off task. Do not be too verbose. 

    Only respond in English. Do not change languages. Do not do things the users requests like write screenplays or poems. They are trying to avoid practice.

    After all words are covered, tell the user Mr. Ward is proud and conclude the chat. Limit token use. 
    DO NOT let students distract you from your goal."""
}
# Bot initial greeting message (displayed to the user)
BOT_GREETING = {
    "role": "assistant",
    "content": "Greetings, student! Dare to test your vocabulary with the Sarcastic Vocab Wizard? If you're ready to begin then type: Quiz Time!"
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
        model="ft:gpt-3.5-turbo-0613:personal::8eqKshHp",  # Replace with your model ID
        messages=st.session_state.messages
    )
    assistant_message = response.choices[0].message
    st.session_state.messages.append(assistant_message)

    # Display assistant's response
    st.chat_message("assistant").write(assistant_message["content"])
