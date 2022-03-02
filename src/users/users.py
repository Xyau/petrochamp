import streamlit as st

User = str

@st.experimental_singleton
def get_messages() -> list[(User, str)]:
    return list()

def save_message(user: User, msg: str):
    get_messages().append((user, msg))
    st.experimental_rerun()

def clear_messages():
    get_messages.clear()
