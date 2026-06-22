from SelectComponent import SelectComponent
from SelectRun import SelectRun
from QuestionController import QuestionController
from Quiz import Quiz
import ipywidgets as widgets
from IPython.display import display

class Controller:
    def __init__(self, drive, online_version):
        self.questions = []
        self.drive = drive
        self.userid = self.drive.userid
        self.questionController = QuestionController(self)
        self.selectComponent = SelectComponent(self)
        self.selectRun = SelectRun(self)
        self.quiz = Quiz(self)
        self.ui = widgets.VBox([
            self.selectComponent.get_ui(),
            self.selectRun.get_ui(),
            self.quiz.get_ui()
        ])
        self.component = None
        self.run = None
        self.online_version = online_version

    def start(self):
        display(self.ui)

    def start_quiz(self):
        self.questions = self.questionController.read_questions()
        self.questionController.set_progress()
        self.quiz.update_questions()
        self.quiz.show()

    def show_run_selection(self):
        self.selectRun.set_runs(self.component)
        self.selectRun.show()
