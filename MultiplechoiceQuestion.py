import ipywidgets as widgets

class MultipleChoiceQuestion:
    def __init__(self, data, controller):
        self.data = data
        self.controller = controller
        self.output = widgets.Output()

        choices = data.get("choices", [])

        title = self.data.get("title", "No title")
        previous = self.controller.questionController.answers.get(title, "unanswered")

        try:
            selected_index = choices.index(previous) if previous in choices else None
        except ValueError:
            selected_index = None

        self.radio = widgets.RadioButtons(
            options=choices,
            description="Choices:",
            style={"description_width": "initial"},
            layout=widgets.Layout(width="100%"),
            index=selected_index
        )

        self.button = widgets.Button(
            description="Submit",
            button_style="primary",
            icon="check"
        )
        self.button.on_click(self.check)

        self.result = widgets.Output()

    def get_ui(self):
        box = widgets.VBox(
            [self.output, self.radio, self.button, self.result],
            layout=widgets.Layout(align_items="flex-start")
        )

        self.render_text()
        return box
    
    def render_text(self):
        self.output.clear_output()

        title = self.data.get("title", "No title")
        previous = self.controller.questionController.answers.get(title, "unanswered")

        with self.output:
            print(title)
            print("-" * 40)
            print(self.data.get("text", ""))
            print("\nPrevious answer:", previous)

    def check(self, _):
        self.result.clear_output()

        correct = self.data.get("correctness", [])
        idx = self.radio.index

        with self.result:
            if idx is None:
                print("No answer selected")
            elif correct[idx]:
                self.controller.questionController.save_answer(self.data.get("title", "No title"),self.data.get("choices", [])[idx], 'correct')
                print("Correct ✅")
            else:
                self.controller.questionController.save_answer(self.data.get("title", "No title"),self.data.get("choices", [])[idx], 'incorrect')
                print("Incorrect ❌")