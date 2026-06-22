import ipywidgets as widgets

class OpenQuestion:
    def __init__(self, data, controller):
        self.data = data
        self.controller = controller
        self.output = widgets.Output()

        saved = self.controller.questionController.answers.get(
            self.data.get("title", "No title"),
            ""
        )

        self.editor = widgets.Textarea(
            value=saved if saved != "unanswered" else "",
            placeholder="Write your answer here...",
            layout=widgets.Layout(width="100%", height="150px")
        )

        self.submit_button = widgets.Button(
            description="Submit",
            button_style="primary",
            icon="check"
        )
        self.submit_button.on_click(self.submit_answer)

        self.result = widgets.Output()

        self.render_text()

    def render_text(self):
        self.output.clear_output()
        with self.output:
            print(self.data.get("title", "No title"))
            print("-" * 40)
            print(self.data.get("text", ""))

    def submit_answer(self, _):
        self.result.clear_output()

        answer = self.editor.value
        self.controller.questionController.save_answer(self.data.get("title", "No title"),answer, 'correct')
        print()

    def get_ui(self):
        return widgets.VBox([
            self.output,
            self.editor,
            self.submit_button,
            self.result
        ])