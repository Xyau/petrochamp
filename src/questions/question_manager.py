import threading

from src.questions.questions import Question
import streamlit as st

class QuestionManager:
    questions: list[Question]
    run_string: str
    lock: threading.Lock
    finished: bool

    def __init__(self):
        self.questions = []
        self.run_string = "No questions loaded"
        self.lock = threading.Lock()
        self.finished = False

    def add_question(self, question: Question):
        with self.lock:
            for present_questions in self.questions:
                if present_questions.get_question_text() == question.get_question_text():
                    return
            self.questions.append(question)

    def get_questions(self) -> list[Question]:
        with self.lock:
            return self.questions.copy()

    def clear_questions(self):
        with self.lock:
            self.finished = False
            self.questions.clear()

# @st.experimental_singleton
# def get_question_manager() -> QuestionManager:
#     return QuestionManager()
