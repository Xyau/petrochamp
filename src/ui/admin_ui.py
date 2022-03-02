from pandas import DataFrame

from src.answers.answers import get_answers_manager, AnswerManager, Answer
from src.constants.constants import NUMBER, SET
from src.db.db import get_all_rows, get_all_rows_base
from src.questions.question_manager import get_question_manager, QuestionManager
from src.questions.questions import Question, TextQuestion
from src.users.users import User
from src.ui import ui
import streamlit as st

def build_active_users_ui():
    answers_manager: AnswerManager = get_answers_manager()
    users = answers_manager.question_start_time_by_user.keys()
    question_manager: QuestionManager = get_question_manager()
    questions = question_manager.get_questions()
    if st.checkbox(label="Hide questions and answers"):
        return
    st.text("Active users")
    for idx, question in enumerate(questions):
        st.markdown(f'Question #{idx}: {question.get_question_text()}')
        st.markdown(f'Answer #{idx}: {question.get_answer_text()}')
        for user in users:
            answer: Answer = answers_manager.get_user_answer(user, question)
            if not answer.is_started():
                st.text(f'{user} did not hear the question yet')
            elif not answer.is_answered():
                st.text(f'{user} did not answer the question yet')
            else:
                st.text(f'{user}: {answer.answer} took {str(answer.time_taken())[:5]}s')

def select_question_ui(key: str):
    print(f'Using key: {key}')
    df: DataFrame = get_all_rows(key)
    set_names = st.multiselect(label="Narrow questions by set name if you want", options=df[SET].unique())
    # question_number = question_filters.selectbox(label="Filter by question number, -1 means no filter",
    #                                              options=df[NUMBER].unique())
    amount = st.number_input(label="Select number of questions to add", min_value=1, max_value=10, value=1)
    if st.button(label=f"Add {amount} random question"):
        if len(set_names) == 0:
            st.text(f'Adding {amount} random questions chosen from all sets')
            raw_questions = df.sample(n=amount)
        else:
            st.text(f'Adding {amount} random questions chosen from {set_names}')
            raw_questions = df[df[SET].isin(set_names)].sample(n=amount)
        st.text(f'Questions selected: {raw_questions}')
        question_dicts: list[dict[str, str]] = raw_questions.to_dict('records')
        question_manager: QuestionManager = get_question_manager()

        for raw_question in question_dicts:
            question: Question = Question.build_question(raw_question)
            if question is None:
                st.text("Failed to add question, check the logs!")
            else:
                question_manager.add_question(question)
                st.text(f'Added question {question} to test set')


def clear_questions_ui():
    if st.sidebar.button(label="Reset answers and questions to answer"):
        question_manager: QuestionManager = get_question_manager()
        question_manager.clear_questions()
        answers_manager: AnswerManager = get_answers_manager()
        answers_manager.clear_all_answers()

def set_admin_ui(user: User, key: str):
    clear_questions_ui()
    select_question_ui(key)
    build_active_users_ui()

