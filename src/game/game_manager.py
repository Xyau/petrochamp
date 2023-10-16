import logging
import threading
from typing import Optional

from src.answers.answers import AnswerManager
from src.questions.question_manager import QuestionManager
from src.users.users import User

import streamlit as st

class GameConfig:
    # If none, you have unlimited seconds
    seconds_to_answer: Optional[int] = 10

class Game:
    question_manager: QuestionManager
    answer_manager: AnswerManager
    users: set[User]
    name: str
    creator: User
    config: GameConfig

    def __init__(self, name: str, config: GameConfig = GameConfig()):
        self.name = name
        self.question_manager = QuestionManager()
        self.answer_manager = AnswerManager()
        self.users = set()
        self.config = config

    def add_user(self, user: User):
        self.users.add(user)

    def __str__(self):
        return self.name

class GameManager:
    games_by_name: dict[str, Game]
    lock: threading.Lock

    def __init__(self):
        self.games_by_name = {}
        self.lock = threading.Lock()

    def create_game(self, game_name: str):
        with self.lock:
            if game_name in self.games_by_name:
                logging.error("Already exists a game with that name")
                return
            else:
                self.games_by_name[game_name] = Game(game_name)

    def get_game(self, game_name: str) -> Game:
        if game_name not in self.games_by_name:
            raise f'No game with this name: {game_name}'
        else:
            return self.games_by_name[game_name]

    def delete_game(self, game_name: str):
        if game_name not in self.games_by_name:
            raise f'No game with this name: {game_name}'
        else:
            self.games_by_name.pop(game_name)

@st.cache_resource
def get_game_manager() -> GameManager:
    return GameManager()
