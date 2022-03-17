import streamlit as st
import src.ui.player_ui as player_ui
import src.ui.admin_ui as admin_ui
from src.game.game_manager import Game
from src.ui import ui

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


game: Game = ui.select_game_ui(is_admin)

if is_admin:
    admin_ui.set_admin_ui(game=game, key=key)
else:
    player_ui.set_player_ui(game=game, user=user)