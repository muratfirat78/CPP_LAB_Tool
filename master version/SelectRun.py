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

        self.new_run_button = widgets.Button(
            description="New run",
            button_style="warning",
            icon="plus"
        )

        self.new_run_input = widgets.Text(
            description="Run:"
        )

        self.confirm_run_button = widgets.Button(
            description="Create",
            button_style="success",
            icon="check"
        )

        self.confirm_run_button.on_click(self.create_new_run)

        self.new_run_box = widgets.VBox([
            self.new_run_input,
            self.confirm_run_button
        ])

        self.new_run_box.layout.display = "none"

        self.new_run_button.on_click(self.new_run)

        self.start_button = widgets.Button(
            description="Continue",
            button_style="success",
            icon="play"
        )

        self.start_button.on_click(self.start)

        self.vbox = widgets.VBox([
            self.run_list,
            self.new_run_box,
            widgets.HBox([self.new_run_button, self.start_button])
        ])
        self.hide()

    def new_run(self, _):
        self.run_list.layout.display = "none"
        self.new_run_box.layout.display = ""

    def create_new_run(self, _):
        run_name = self.new_run_input.value.strip()
        component = self.quiz.component

        if not run_name:
            print("Run name cannot be empty")
            return

        source_run = self.run_list.value

        if source_run:
            self.copy_run(source_run, run_name)

        self.new_run_input.value = ""
        self.new_run_box.layout.display = "none"
        self.run_list.layout.display = ""

        current = list(self.run_list.options)
        current.append(run_name)
        self.run_list.options = sorted(set(current))
        self.run_list.value = run_name

    def get_ui(self):
        return self.vbox

    def hide(self):
        self.run_list.layout.display = "none"
        self.start_button.layout.display = "none"
        self.new_run_button.layout.display = "none"

    def show(self):
        self.run_list.layout.display = ""
        self.start_button.layout.display = ""
        self.new_run_button.layout.display = ""

    def set_runs(self, component):
        runs = set()

        for filename in os.listdir("../questions"):
            with open(f"../questions/{filename}", encoding="utf-8") as f:
                data = json.load(f)

                if data["component"] == component:
                    runs.add(data["run"])
        self.run_list.options = sorted(runs)

    def copy_run(self, source_run, new_run):
        component = self.quiz.component

        for filename in os.listdir("../questions"):
            path = f"../questions/{filename}"

            with open(path, encoding="utf-8") as f:
                data = json.load(f)

            if data["component"] == component and data["run"] == source_run:
                new_data = data.copy()
                new_data["run"] = new_run

                # build new filename
                new_filename = filename.replace(source_run, new_run)

                with open(f"../questions/{new_filename}", "w", encoding="utf-8") as f:
                    json.dump(new_data, f, indent=2, ensure_ascii=False)

    def start(self,_):
        self.quiz.run = self.run_list.value
        self.hide()
        self.quiz.start_quiz()