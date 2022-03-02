from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from src.constants.constants import NUMBER, SET_NUMBER, SET, QUESTION, ANSWER, ANSWER_TYPE


@dataclass
class QuestionInfo:
    question_text: str
    answer_text: str
    number: str
    set_name: str
    set_number: str

class AnswerType(Enum):
    TEXT = auto(),

class Question(ABC):
    def get_question_text(self) -> str:
        return self.get_question_info().question_text

    def get_answer_text(self) -> str:
        return self.get_question_info().answer_text

    @abstractmethod
    def answer_is_correct(self, user_answer: str) -> float:
        pass

    @abstractmethod
    def get_question_info(self) -> QuestionInfo:
        pass

    def __str__(self):
        return str(self.get_question_info())

    @staticmethod
    def build_question(raw: dict[str, str]) -> Optional[Question]:
        if NUMBER not in raw:
            logging.error(f'{NUMBER} not in raw: {raw}')
            return None
        if SET not in raw:
            logging.error(f'{SET} not in raw: {raw}')
            return None
        if SET_NUMBER not in raw:
            logging.error(f'{SET_NUMBER} not in raw: {raw}')
            return None
        if QUESTION not in raw:
            logging.error(f'{QUESTION} not in raw: {raw}')
            return None
        if ANSWER not in raw:
            logging.error(f'{ANSWER} not in raw: {raw}')
            return None

        question_info = QuestionInfo(raw[QUESTION], raw[ANSWER], raw[NUMBER], raw[SET], raw[SET_NUMBER])

        # if ANSWER_TYPE not in raw or raw[ANSWER_TYPE] == AnswerType.TEXT.name:
        return TextQuestion(question_info)

class TextQuestion(Question):
    info: QuestionInfo

    def __init__(self, info: QuestionInfo):
        self.info = info

    def answer_is_correct(self, user_answer: str) -> float:
        return self.info.answer_text.strip().lower() == user_answer.strip().lower()

    def get_question_info(self) -> QuestionInfo:
        return self.info

