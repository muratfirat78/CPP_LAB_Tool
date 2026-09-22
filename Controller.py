from SelectComponent import SelectComponent
from SelectRun import SelectRun
from QuestionController import QuestionController
from Quiz import Quiz
import ipywidgets as widgets
from IPython.display import display
import sys
import os

class Controller:
    def __init__(self, drive, online_version):
        self.questions = []
        self.drive = drive
        self.userid = self.drive.userid
        self.questionController = QuestionController(self)
        self.selectComponent = SelectComponent(self)
        self.selectRun = SelectRun(self)
        self.quiz = Quiz(self)
        self.dashboard_tab = widgets.Output()
        # self.tabs = widgets.Tab([self.quiz.get_ui(), self.dashboard_tab])
        self.tabs = widgets.Tab([self.quiz.get_ui(), self.dashboard_tab])
        self.tabs.layout.display = 'none'
        self.tabs.set_title(0, 'Quiz')
        self.tabs.set_title(1, 'Dashboard')
        self.tabs.layout.display = 'none'
        self.ui = widgets.VBox([
            self.selectComponent.get_ui(),
            self.selectRun.get_ui(),
            self.tabs
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
        
        if self.component == "Data Understanding and Data Preparation":
            self.tabs.children = [self.quiz.get_ui(), self.dashboard_tab]
            self.tabs.set_title(0, 'Quiz')
            self.tabs.set_title(1, 'Dashboard')
            self._load_dashboard()
        else:
            self.tabs.children = [self.quiz.get_ui()]
            self.tabs.set_title(0, 'Quiz')
        
        self.tabs.layout.display = 'block'

    def _load_dashboard(self):
        dashboard_path = os.path.join(os.getcwd(), "Statistics_Dashboard")
        if dashboard_path not in sys.path:
            sys.path.insert(0, dashboard_path)
        try:
            from Visual import VisualManager
            VisManager = VisualManager()
            dashboard = widgets.Tab([
                VisManager.generateSamplingTab(),
                VisManager.generateHTTab(),
                VisManager.generateANTAB()
            ])
            dashboard.set_title(0, 'Sampling')
            dashboard.set_title(1, 'Hypothesis Testing')
            dashboard.set_title(2, 'ANOVA')
            with self.dashboard_tab:
                display(dashboard)
        except Exception as e:
            with self.dashboard_tab:
                print("Dashboard kon niet worden geladen:", e)

    def show_run_selection(self):
        self.selectRun.set_runs(self.component)
        self.selectRun.show()