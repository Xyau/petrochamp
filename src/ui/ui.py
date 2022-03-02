

import time

import streamlit as st

from src.audio import audio
from src.audio.audio import AudioCache
from src.answers.answers import AnswerManager, Answer, get_answers_manager
from src.questions.questions import Question
from src.users.users import User

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

def add_question(user: str, question: Question) -> Answer:
    audio_cache: AudioCache = audio.get_audio_cache()
    answer_manager: AnswerManager = get_answers_manager()

    st.text(question.get_question_text())
    previous_answer = answer_manager.get_user_answer(user, question)
    answer_txt = st.text_input("Answer", key=question.get_question_text().__hash__())
    if not previous_answer.is_started():
        audio_bytes = audio_cache.get_text_audio(question.get_question_text())
        answer = answer_manager.user_started_question(user, question)
        autoplay_audio(audio_bytes.builtin_bytes)
        st.audio(audio_bytes.bytes_io)
        return answer
    elif not previous_answer.is_answered() and len(answer_txt) != 0:
        return answer_manager.user_finished_question(user, question, answer_txt)
    else:
        return previous_answer


def start_question_run(user: User, current_questions: list[Question], is_finished: bool = False) -> bool:
    total_time = 0.0
    correct_number = 0
    for question in current_questions:
        answer: Answer = add_question(user, question)
        if answer.is_answered():
            total_time += answer.time_taken()
            is_correct = question.answer_is_correct(answer.answer)
            correct_number += 1 if is_correct else 0
            if is_correct:
                st.markdown(f'You answered: \"{answer.answer}\" correctly and it took: {str(answer.time_taken())[:4]}s to answer')
            else:
                st.markdown(f'You answered: \"{answer.answer}\" incorrectly, the correct answer is'
                        f' \"{question.get_answer_text()}\" and it took: {str(answer.time_taken())[:4]}s to answer')
        else:
            return False
    if not is_finished:
        st.markdown(f'Wait for the host to send the next question!')
    else:
        st.markdown(f'You finished all questions! You got {correct_number}/{len(current_questions)} in {str(total_time)[:4]}s')

