import openai
import streamlit as st

st.title("Chat Bot (GPT-3.5)")

openai.api_key = secrets["OPENAI_API_KEY"]

# System prompt configuration
SYSTEM_PROMPT = {
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

If a student says 'thanks for the fun', reply 'Mr. Ward is proud of you!' and end the chat. After all words are covered, tell the user Mr. Ward is proud and conclude the chat. Limit token use."""

}

# Initialize the conversation with the system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_PROMPT]

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["ft:gpt-3.5-turbo-0613:personal::8XHlpNEE"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
