import time

from src.answers.answers import Answer, AnswerManager
from src.audio import audio
from src.audio.audio import AudioCache
from src.game.game_manager import Game
from src.questions.questions import Question
from src.users.users import User
import streamlit as st


def autoplay_audio(audio_bytes: bytes):
    mymidia_placeholder = st.empty()
    mymidia_str = "data:audio/ogg;base64,%s" % (audio_bytes)
    mymidia_html = """
                    <audio autoplay class="stAudio">
                    <source src="%s" type="audio/ogg">
                    Your browser does not support the audio element.
                    </audio>
                """ % mymidia_str
    mymidia_placeholder.empty()
    time.sleep(1)
    mymidia_placeholder.markdown(mymidia_html, unsafe_allow_html=True)


def add_question(user: str, question: Question, answer_manager: AnswerManager) -> Answer:
    audio_cache: AudioCache = audio.get_audio_cache()
    previous_answer = answer_manager.get_user_answer(user, question)
    # if previous_answer.is_finished():
    st.markdown(question.get_question_text())
    audio_bytes = audio_cache.get_text_audio(question.get_question_text())
    st.audio(audio_bytes.bytes_io)

    answer_txt = st.text_input("Answer", key=question.get_question_text().__hash__(),
                               disabled=previous_answer.is_answered() | previous_answer.is_finished())
    if not previous_answer.is_started():
        answer = answer_manager.user_started_question(user, question)
        autoplay_audio(audio_bytes.builtin_bytes)
        st.button("Skip", args=None, on_click=lambda: answer_manager.user_finished_question(user, question))
        return answer
    elif not previous_answer.is_finished() and len(answer_txt) != 0:
        return answer_manager.user_finished_question(user, question, answer_txt)
    else:
        return previous_answer


def start_question_run(user: User, game: Game) -> bool:
    total_time = 0.0
    correct_number = 0
    questions: list[Question] = game.question_manager.get_questions()

    for idx, question in enumerate(questions):
        st.markdown(f'Question #{idx}')
        answer: Answer = add_question(user, question, game.answer_manager)
        if answer.is_finished():
            if answer.is_answered():
                total_time += answer.time_taken()
                is_correct = question.answer_is_correct(answer.answer)
                correct_number += 1 if is_correct else 0
                if is_correct:
                    st.markdown(
                        f'You answered: \"{answer.answer}\" correctly and it took: {str(answer.time_taken())[:4]}s to answer')
                else:
                    st.markdown(f'You answered: \"{answer.answer}\" incorrectly, the correct answer is'
                                f' \"{question.get_answer_text()}\" and it took: {str(answer.time_taken())[:4]}s to answer')
            else:
                st.markdown(f'You skipped the question, the correct answer is'
                            f' \"{question.get_answer_text()}\"')
        else:
            return False
        st.markdown("***")
    st.markdown(f'Wait for the host to send the next question!')


def set_player_ui(game: Game, user: User):
    start_question_run(user, game)
