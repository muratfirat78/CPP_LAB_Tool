import ipywidgets as widgets

class OpenQuestion:
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

        self.correctness = widgets.Textarea(
            value=data.get("correctness", ""),
            description="Answer:",
            layout=widgets.Layout(width="100%", height="150px")
        )

        self.save_question_button = widgets.Button(
            description="Save question",
            button_style="success",
            icon="save"
        )

        self.save_question_button.on_click(self.save_question)

        self.ui = widgets.VBox([
            self.title,
            self.text,
            self.index,
            self.correctness,
            self.save_question_button
        ])

    def get_data(self):
        return {
            "title": self.title.value,
            "text": self.text.value,
            "index": self.index.value,
            "type": "open",
            "correctness": self.correctness.value
        }

    def save_question(self, event):
        data = self.get_data()
        self.controller.questionController.save_question(data)
    
    def get_data(self):
        return {
            "title": self.title.value,
            "text": self.text.value,
            "index": self.index.value,
            "type": "open",
            "correctness": self.correctness.value
        }

    def get_ui(self):
        return self.ui