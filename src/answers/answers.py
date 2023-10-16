import time
from dataclasses import dataclass

from src.questions.questions import Question
from src.users.users import User

import streamlit as st

@dataclass
class Answer:
    start_time: float = None
    end_time: float = None
    answer: str = None

    def is_started(self) -> bool:
        return self.start_time is not None

    def is_answered(self) -> bool:
        return self.answer is not None

    def time_taken(self) -> float:
        return self.end_time - self.start_time

    def is_finished(self) -> bool:
        return self.end_time is not None

class AnswerManager:
    question_start_time_by_user: dict[User, dict[str, Answer]]

    def __init__(self):
        self.question_start_time_by_user = {}

    def user_started_question(self, user: User, question: Question) -> Answer:
        if user not in self.question_start_time_by_user:
            self.question_start_time_by_user[user] = {}
        answer = Answer(time.time())
        self.question_start_time_by_user[user][question.get_question_text()] = answer
        return answer

    def user_finished_question(self, user: User, question: Question, answer_str: str = None) -> Answer:
        start = self.question_start_time_by_user[user][question.get_question_text()].start_time
        end = time.time()
        answer = Answer(start, end, answer_str)
        self.question_start_time_by_user[user][question.get_question_text()] = answer
        return answer

    def get_user_answer(self, user: User, question: Question) -> Answer:
        if user not in self.question_start_time_by_user:
            return Answer()
        if question.get_question_text() not in self.question_start_time_by_user[user]:
            return Answer()
        return self.question_start_time_by_user[user][question.get_question_text()]

    def clear_all_answers(self):
        self.question_start_time_by_user = {}

