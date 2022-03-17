from pandas import DataFrame

from src.answers.answers import AnswerManager, Answer
from src.constants.constants import NUMBER, SET
from src.db.db import get_all_rows, get_all_rows_base
from src.game.game_manager import Game
from src.questions.question_manager import QuestionManager
from src.questions.questions import Question, TextQuestion
from src.users.users import User
import streamlit as st
import src.db.db as db


def build_active_users_ui(game: Game):
    answers_manager: AnswerManager = game.answer_manager
    users = answers_manager.question_start_time_by_user.keys()
    question_manager: QuestionManager = game.question_manager
    questions = question_manager.get_questions()
    if st.checkbox(label="Hide questions and answers"):
        return
    st.markdown("Active users:")
    for idx, question in enumerate(questions):
        st.markdown(f'**Question #{idx}**: {question.get_question_text()}')
        st.markdown(f'**Answer #{idx}**: {question.get_answer_text()}')
        for user in users:
            answer: Answer = answers_manager.get_user_answer(user, question)
            if not answer.is_started():
                st.text(f'{user} did not hear the question yet')
            elif not answer.is_finished():
                st.text(f'{user} did not answer the question yet')
            elif answer.is_answered():
                st.text(f'{user}: {answer.answer} took {str(answer.time_taken())[:5]}s')
            else:
                st.text(f'{user} skipped the question')
        st.markdown("***")


def select_question_ui(game: Game, key: str):
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
        question_manager: QuestionManager = game.question_manager

        for raw_question in question_dicts:
            question: Question = Question.build_question(raw_question)
            if question is None:
                st.text("Failed to add question, check the logs!")
            else:
                question_manager.add_question(question)
                st.text(f'Added question {question} to test set')


def clear_questions_ui(game: Game):
    if st.sidebar.button(label="Reset answers and questions to answer"):
        question_manager: QuestionManager = game.question_manager
        question_manager.clear_questions()
        answers_manager: AnswerManager = game.answer_manager
        answers_manager.clear_all_answers()


def set_admin_ui(game: Game, key: str):
    if st.sidebar.button("Reload questions from sheets"):
        db.refresh_questions()

    clear_questions_ui(game=game)
    select_question_ui(game=game, key=key)
    build_active_users_ui(game=game)

