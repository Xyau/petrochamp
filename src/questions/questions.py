from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Union

from src.constants.constants import NUMBER, QUESTION, ANSWER, SETS


@dataclass
class QuestionInfo:
    question_text: str
    answer_text: str
    number: str
    sets: set[str]

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
    def build_question(raw: dict[str, Union[str, set[str]]]) -> Optional[Question]:
        if NUMBER not in raw:
            logging.error(f'{NUMBER} not in raw: {raw}')
            return None
        if SETS not in raw:
            logging.error(f'{SETS} not in raw: {raw}')
            return None
        if QUESTION not in raw:
            logging.error(f'{QUESTION} not in raw: {raw}')
            return None
        if ANSWER not in raw:
            logging.error(f'{ANSWER} not in raw: {raw}')
            return None

        question_info = QuestionInfo(raw[QUESTION], raw[ANSWER], raw[NUMBER], raw[SETS])

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

