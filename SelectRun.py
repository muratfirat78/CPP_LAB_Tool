import ipywidgets as widgets
import os
import json

class SelectRun:
    def __init__(self, quiz):
        self.quiz = quiz

        self.run_list = widgets.Dropdown(
            options=[],
            description="Run:"
        )

        self.start_button = widgets.Button(
            description="Continue",
            button_style="success",
            icon="play"
        )

        self.start_button.on_click(self.start)

        self.vbox = widgets.VBox([
            self.run_list,
            self.start_button
        ])
        self.hide()

    def get_ui(self):
        return self.vbox

    def hide(self):
        self.run_list.layout.display = "none"
        self.start_button.layout.display = "none"

    def show(self):
        self.run_list.layout.display = ""
        self.start_button.layout.display = ""

    def set_runs(self, component):
        runs = set()

        for filename in os.listdir("./questions"):
            with open(f"./questions/{filename}", encoding="utf-8") as f:
                data = json.load(f)

                if data["component"] == component:
                    runs.add(data["run"])

        self.run_list.options = sorted(runs)

    def start(self,_):
        self.quiz.run = self.run_list.value
        self.hide()
        self.quiz.start_quiz()