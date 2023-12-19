# Importing required packages
import streamlit as st
import openai
import uuid
import time

# Set up the page
st.set_page_config(page_title="Sarcastic Vocab Wizard")
st.sidebar.title("Sarcastic Vocab Wizard")
st.sidebar.divider()

# Custom styles for the input box
input_box_styles = """
<style>
.stTextInput > div > div > input {
    font-size: 16px;
    height: 50px;
    border: 2px solid #007BFF;
    border-radius: 5px;
}
</style>
"""
st.markdown(input_box_styles, unsafe_allow_html=True)

# Initialize OpenAI client and set the API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Your chosen fine-tuned model
MODEL = "ft:gpt-3.5-turbo-0613:personal::8XHlpNEE"  # Replace with your fine-tuned model ID

# Initialize session state variables
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "run" not in st.session_state:
    st.session_state.run = {"status": None}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retry_error" not in st.session_state:
    st.session_state.retry_error = 0

# Define your system prompt here
SYSTEM_PROMPT = """You are the Sarcastic Vocab Wizard, here to assess vocabulary knowledge. Present a word from the list, ask the student to use it in a sentence, and provide sarcastic yet constructive feedback if needed. Allow multiple attempts before showing an example sentence. Revisit difficult words for another try. Use humor to ensure understanding, but keep it concise. The vocabulary words:

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

If a student says 'thanks for the fun', reply 'Mr. Ward is proud of you!' and end the chat. After all words are covered, tell the user Mr. Ward is proud and conclude the chat. Limit token use."""

# Chat input and message creation
if prompt := st.chat_input("How can I help you?"):
    with st.chat_message('user'):
        st.write(prompt)

    # Combine the system prompt with the user's prompt
    combined_prompt = SYSTEM_PROMPT + prompt

    # Call to OpenAI API with the fine-tuned model and the combined prompt
    # Assuming openai is already imported and API key is set
try:
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": prompt}],
        max_tokens=150  # Adjust as needed
    )
    assistant_reply = response['choices'][0]['message']['content'] if response['choices'] else "No response."

    with st.chat_message('assistant'):
        st.write(assistant_reply)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Retry logic and other parts of your code remain the same


    # Retry logic as needed (can be customized)
    if st.session_state.retry_error < 3:
        time.sleep(1)
        st.rerun()
