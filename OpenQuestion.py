import ipywidgets as widgets

class OpenQuestion:
    def __init__(self, data, controller):
        self.data = data
        self.controller = controller
        self.output = widgets.Output(layout=widgets.Layout(width="100%"))

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
        self.answer_output = widgets.Output(layout=widgets.Layout(width="100%"))

        self.render_text()

    def render_text(self):
        self.output.clear_output()
        with self.output:
            from IPython.display import display, HTML
            display(HTML(f"""
                <b>{self.data.get("title", "No title")}</b>
                <hr>
                <p style="white-space: pre-wrap;">{self.data.get("text", "")}</p>
            """))

    def submit_answer(self, _):
        self.result.clear_output()
        answer = self.editor.value
        self.controller.questionController.save_answer(self.data.get("title", "No title"), answer, 'correct')

        model_answer = self.data.get("answer", None)
        self.answer_output.clear_output()
        if model_answer:
            with self.answer_output:
                from IPython.display import display, HTML
                display(HTML(f"""
                    <div style="background:#f0f7ff; border-left:4px solid #2196F3; padding:10px; margin-top:10px;">
                        <b>Model answer:</b><br>
                        <p style="white-space: pre-wrap;">{model_answer}</p>
                    </div>
                """))

    def get_ui(self):
        return widgets.VBox([
            self.output,
            self.editor,
            self.submit_button,
            self.result,
            self.answer_output
        ])