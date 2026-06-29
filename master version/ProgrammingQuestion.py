import ipywidgets as widgets

class ProgrammingQuestion:
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
            layout=widgets.Layout(width="100%", height="150px")
        )

        self.index = widgets.IntText(
            value=data.get("index", 0),
            description="Index:"
        )

        self.solution = widgets.Textarea(
            value="\n".join(data.get("solution", [])),
            description="Solution:",
            layout=widgets.Layout(width="100%", height="200px")
        )

        self.tests_box = widgets.VBox()

        tests = data.get("tests", {})

        for key, value in tests.items():
            self.add_test_row(key, value)

        self.add_test_button = widgets.Button(
            description="Add test",
            button_style="info",
            icon="plus"
        )

        self.add_test_button.on_click(
            lambda _: self.add_test_row()
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
            widgets.HTML("<h4>Tests</h4>"),
            self.tests_box,
            self.add_test_button,
            widgets.HTML("<h4>Solution</h4>"),
            self.solution,
            self.save_button
        ])

    def add_test_row(self, key="", value=""):

        key_widget = widgets.Text(
            value=str(key),
            description="Key:"
        )

        value_widget = widgets.Text(
            value=str(value),
            description="Expected:"
        )

        remove_button = widgets.Button(
            description="Remove",
            button_style="danger",
            icon="trash"
        )

        row = widgets.HBox([
            key_widget,
            value_widget,
            remove_button
        ])

        def remove(_):
            self.tests_box.children = tuple(
                child
                for child in self.tests_box.children
                if child is not row
            )

        remove_button.on_click(remove)

        self.tests_box.children = (
            self.tests_box.children + (row,)
        )

    def get_data(self):

        tests = {}

        for row in self.tests_box.children:
            key_widget, value_widget, _ = row.children

            if key_widget.value.strip():
                tests[key_widget.value] = value_widget.value

        return {
            "title": self.title.value,
            "text": self.text.value,
            "index": self.index.value,
            "type": "programming",
            "tests": tests,
            "solution": self.solution.value.splitlines()
        }

    def save_question(self, _):
        self.controller.questionController.save_question(
            self.get_data()
        )

    def get_ui(self):
        return self.ui