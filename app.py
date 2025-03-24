import os
import streamlit as st
import google.generativeai as genai
import time

f = open("keys/gemini.txt")
api_key = f.read()

if not api_key:
    st.error('Gen AI API key not found. Please set the GENAI_API_KEY environment variable.')
    st.stop()

# Configure Gen AI with the API key
genai.configure(api_key=api_key)

st.title("💬 SMenAI !!! Generative Data Science Chatbot")

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              system_instruction="""You are a helpful Data Science AI Teaching Assistant. Your name is "Smen" developed by Soumen.
                              Given a topic that is related to Data Science whatever comes, You assist all queries and if it's not related to computer 
                              science then tell 'This is beyond my knowledge.""")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

chat = model.start_chat(history=st.session_state["chat_history"])

for msg in chat.history:
    st.chat_message(msg.role).write(msg.parts[0].text)

user_prompt = st.chat_input()

if user_prompt:
    st.chat_message('user').write(user_prompt)

    # Display loading message
    with st.chat_message("ai"):
        st.text("Smen is typing")
        placeholder = st.empty()
        full_response = chat.send_message(user_prompt).text

        # Simulate typing *within* the placeholder
        typed_text = ""
        for char in full_response:
            typed_text += char
            placeholder.markdown(f"Smen is typing... {typed_text}", unsafe_allow_html=True) 
            time.sleep(0.001)

        # Final update after typing is complete 
        placeholder.markdown(full_response, unsafe_allow_html=True)  

    st.session_state["chat_history"] = chat.history
