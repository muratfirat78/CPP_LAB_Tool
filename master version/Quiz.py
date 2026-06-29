import ipywidgets as widgets
from IPython.display import display
from OpenQuestion import OpenQuestion
from MultipleChoiceQuestion import MultipleChoiceQuestion
from ProgrammingQuestion import ProgrammingQuestion
from Overview import Overview

class Quiz:
    def __init__(self, controller):
        self.controller = controller
        self.ignore_select = False
        self.overview = Overview(controller)

        self.question_list = widgets.Select(
            options=[],
            description="Questions:",
            layout=widgets.Layout(flex="0 0 300px", height="400px")
        )

        self.question_display = widgets.Output(
            layout=widgets.Layout(flex="1 1 auto", border="1px solid #ddd", padding="10px")
        )

        self.question_type = widgets.Dropdown(
            options=[
                ("Open", "open"),
                ("Multiple Choice", "multiple_choice"),
                ("Programming", "programming")
            ],
            value="open",
            description="Type:"
        )

        self.new_question_button = widgets.Button(
            description="New Question",
            button_style="success",
            icon="plus"
        )

        self.delete_question_button = widgets.Button(
            description="Delete question",
            button_style="danger",
            icon="trash"
        )

        self.delete_question_button.on_click(self.delete_question)
        
        self.new_question_button.on_click(self.create_question)

        self.left_panel = widgets.VBox([
            self.question_type,
            self.new_question_button,
            self.delete_question_button,
            self.question_list
        ])

        # self.overview_display = widgets.Output()

        self.tabs = widgets.Tab(children=[
            widgets.HBox([
                self.left_panel,
                self.question_display
            ]),
            self.overview.get_ui()
        ])

        self.tabs.set_title(0, "Question")
        self.tabs.set_title(1, "Progress overview")

        self.ui = self.tabs

        self.question_list.observe(self.on_select, names="value")
        self.hide()

    def delete_question(self, _):
        idx = self.question_list.value

        if idx is None:
            return

        question = self.controller.questions[idx]

        self.controller.questionController.delete_question(
            question["index"]
        )

        self.controller.questions = (
            self.controller.questionController.read_questions()
        )

        self.update_questions()

        self.question_display.clear_output()


    def create_question(self, _):
        qtype = self.question_type.value

        if qtype == "open":
            new_question = {
                "title": "New Question",
                "text": "",
                "index":self.controller.get_next_index(),
                "type": "open",
                "solution": []
            }

        elif qtype == "multiple_choice":
            new_question = {
                "title": "New Question",
                "text": "",
                "index":self.controller.get_next_index(),
                "type": "multiple_choice",
                "options": [],
                "correct": [],
                "solution": []
            }

        elif qtype == "programming":
            new_question = {
                "title": "New Question",
                "text": "",
                "index":self.controller.get_next_index(),
                "component": "",
                "run": "",
                "type": "programming",
                "tests": {},
                "solution": []
            }

        self.controller.questions.append(new_question)

        self.update_questions()

        idx = len(self.controller.questions) - 1

        self.ignore_select = True
        self.question_list.value = idx
        self.ignore_select = False

        self.render_question(new_question)

    def show(self):
        self.ui.layout.display = ""

    def hide(self):
        self.ui.layout.display = "none"

    def get_ui(self):
        return self.ui
    
    def update_questions(self):
        overview = self.controller.questionController.overview
        selected = self.question_list.value 
        self.ignore_select = True

        self.question_list.options = [
            (q["title"], i) for i, q in enumerate(self.controller.questions)
        ]

        if selected is not None and selected < len(self.controller.questions):
            self.ignore_select = True
            self.question_list.value = selected
        self.ignore_select = False

    def on_select(self, change):
        if self.ignore_select:
            self.ignore_select = False
        else:
            if change["name"] != "value":
                return

            id = change["new"]
            if id is None:
                return
            question = self.controller.questions[id]
            self.render_question(question)

    def render_question(self, question_data):
        self.question_display.clear_output()
        if question_data["type"] == "open":
            q = OpenQuestion(question_data, self.controller)
        elif question_data["type"] == "multiple_choice":
            q = MultipleChoiceQuestion(question_data,self.controller)
        elif question_data["type"] == "programming":
            q = ProgrammingQuestion(question_data,self.controller)
        else:
            raise ValueError("Unknown type")

        with self.question_display:
            display(q.get_ui())