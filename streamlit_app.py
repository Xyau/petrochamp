import streamlit as st
from pandas import DataFrame
import src.db.db as db
import src.users.users as users
from src.questions.question_manager import get_question_manager, QuestionManager
from src.questions.questions import Question, TextQuestion
from src.utils.utils import get_dataframe_info
import src.ui.player_ui as player_ui
import src.ui.admin_ui as admin_ui

st.title("Petrochamp petrobowl training")
login = st.form("Login data")
key = login.text_input(label="Please input the key to decrypt the connection info :)"
                             "It should be on the GSheet, in the README sheet")
user = login.text_input(label="Username")
is_admin = login.checkbox(label="Check if you are admin", value=False)
login.form_submit_button()

if len(key) == 0 or len(user) == 0:
    st.warning("Please fill Login Data to start")
    st.stop()

if st.sidebar.button("Reload questions from sheets"):
    db.refresh_questions()

# if st.sidebar.button("Clear chat"):
#     users.clear_messages()
#
# st.sidebar.text("Chat:")
# msgs = users.get_messages()
# for usr, msg in msgs:
#     st.sidebar.info(f'{usr}: {msg}')
# msg = st.sidebar.text_input("Type msg here")
# if st.sidebar.button("Send MESSAGE"):
#     users.save_message(user=user, msg=msg)

if is_admin:
    admin_ui.set_admin_ui(user, key)
else:
    player_ui.set_player_ui(user)