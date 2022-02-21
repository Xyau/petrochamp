import streamlit as st

@st.experimental_singleton
def get_messages() -> list[(str, str)]:
    return list()

def save_message(user: str, msg: str):
    get_messages().append((user, msg))
    st.experimental_rerun()

def clear_messages():
    get_messages.clear()