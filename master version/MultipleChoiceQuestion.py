import ipywidgets as widgets

class MultipleChoiceQuestion:
    def __init__(self, data, controller):
        self.data = data
        self.controller = controller

        self.title = widgets.Text(
            value=data.get("title", ""),
            description="Title:"
        )

        self.text = widgets.Textarea(
            value=data.get("text", ""),
            description="Text:",
            layout=widgets.Layout(width="100%", height="120px")
        )

        self.index = widgets.IntText(
            value=data.get("index", 0),
            description="Index:"
        )

        self.options_box = widgets.VBox()

        choices = data.get("choices", [])
        correctness = data.get("correctness", [])

        for i, choice in enumerate(choices):
            correct = correctness[i] if i < len(correctness) else False
            self.add_option_row(choice, correct)

        self.add_option_button = widgets.Button(
            description="Add option",
            button_style="info",
            icon="plus"
        )
        self.add_option_button.on_click(
            lambda _: self.add_option_row()
        )

        self.save_button = widgets.Button(
            description="Save question",
            button_style="success",
            icon="save"
        )
        self.save_button.on_click(self.save_question)

        self.ui = widgets.VBox([
            self.title,
            self.text,
            self.index,
            widgets.HTML("<h4>Options</h4>"),
            self.options_box,
            self.add_option_button,
            self.save_button
        ])

    def add_option_row(self, text="", correct=False):

        option_text = widgets.Text(
            value=text,
            description="Option:"
        )

        option_correct = widgets.Checkbox(
            value=correct,
            description="Correct"
        )

        remove_button = widgets.Button(
            description="Remove",
            button_style="danger",
            icon="trash"
        )

        row = widgets.HBox([
            option_text,
            option_correct,
            remove_button
        ])

        def remove(_):
            self.options_box.children = tuple(
                child
                for child in self.options_box.children
                if child is not row
            )

        remove_button.on_click(remove)

        self.options_box.children = (
            self.options_box.children + (row,)
        )

    def get_data(self):

        choices = []
        correctness = []

        for row in self.options_box.children:
            option_text, option_correct, _ = row.children

            choices.append(option_text.value)
            correctness.append(option_correct.value)

        return {
            "title": self.title.value,
            "text": self.text.value,
            "index": self.index.value,
            "type": "multiple_choice",
            "choices": choices,
            "correctness": correctness
        }

    def save_question(self, _):
        self.controller.questionController.save_question(
            self.get_data()
        )

    def get_ui(self):
        return self.ui