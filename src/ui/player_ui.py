from src.questions.question_manager import get_question_manager, QuestionManager
from src.questions.questions import Question
from src.users.users import User
from src.ui import ui


def set_player_ui(user: User):
    question_manager: QuestionManager = get_question_manager()
    questions: list[Question] = question_manager.get_questions()

    ui.start_question_run(user, questions, question_manager.get_finished())
