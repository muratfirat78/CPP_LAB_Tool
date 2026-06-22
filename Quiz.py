import ipywidgets as widgets
from IPython.display import display
from OpenQuestion import OpenQuestion
from MultiplechoiceQuestion import MultipleChoiceQuestion
from ProgrammingQuestion import ProgrammingQuestion

class Quiz:
    def __init__(self, controller):
        self.controller = controller
        self.ignore_select = False

        self.user_label = widgets.HTML(
            value=f"<b>User ID:</b> {self.controller.userid}",
            layout=widgets.Layout(margin="0 0 10px 0")
        )

        self.question_list = widgets.Select(
            options=[],
            description="Questions:",
            layout=widgets.Layout(flex="0 0 300px", height="400px")
        )

        self.question_display = widgets.Output(
            layout=widgets.Layout(flex="1 1 auto", border="1px solid #ddd", padding="10px")
        )

        self.left_panel = widgets.VBox([
            self.user_label,
            self.question_list
        ])

        self.ui = widgets.HBox([
            self.left_panel,
            self.question_display
        ])

        self.question_list.observe(self.on_select, names="value")
        self.hide()

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

        def format_label(q):
            title = q["title"]
            status = overview.get(title, "unanswered")

            if status == "correct":
                marker = "✔️"
            elif status == "incorrect":
                marker = "❌"
            else:
                marker = ""

            return f"{marker} {title}"

        self.question_list.options = [
            (format_label(q), i) for i, q in enumerate(self.controller.questions)
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