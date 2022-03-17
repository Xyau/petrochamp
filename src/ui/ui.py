from typing import Any, Optional

import streamlit as st

from src.game.game_manager import get_game_manager, Game

NONE = "None"

def choose_option(label: str, options: [Any], default: Any = None, add_none: bool = True) -> Optional[Any]:
    options_map = {str(option): option for option in list(options) + ([default] if default is not None else [])}
    options = list(options_map.keys())
    if add_none:
        if default is None:
            options.insert(0, NONE)

    selected_option: str = st.selectbox(label=label, options=options, index=0 if default is None else len(options))
    if selected_option == NONE:
        return None
    else:
        return options_map[selected_option]

def select_game_ui(admin: bool = False) -> Game:
    game_manager = get_game_manager()
    available_games: list[Game] = list(game_manager.games_by_name.values())

    if admin:
        col1, col2 = st.columns(2)
        game_name = col1.text_input("New Game Name").strip()
        if len(game_name) > 2:
            if col2.button("Create!"):
                game_manager.create_game(game_name)
                st.markdown("Successfully created game!")
                st.button("Ok!")
                st.stop()

    col3, col4 = st.columns(2)
    with col3:
        selected_game: Game = choose_option("Select one of the available games:", available_games)
        if selected_game is None:
            st.stop()

    if admin:
        if col4.button("Delete selected game"):
            game_manager.delete_game(selected_game.name)
            st.markdown("Successfully deleted game!")
            st.button("Ok!")
            st.stop()

    return selected_game

