import ipywidgets as widgets

class ProgrammingQuestion:
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
            placeholder="Write Python code here...",
            layout=widgets.Layout(width="100%", height="200px")
        )

        self.submit_button = widgets.Button(
            description="Submit",
            button_style="primary",
            icon="check"
        )
        self.submit_button.on_click(self.submit)

        self.run_output = widgets.Output()

    def get_codecell(self):
        if self.controller.online_version:
            from google.colab import _message
            notebook_json = _message.blocking_request('get_ipynb', request='', timeout_sec=5)
            code_lines = notebook_json["ipynb"]["cells"][2]["source"]
        else:
            import nbformat

            with open("main.ipynb") as f:
                nb = nbformat.read(f, as_version=4)

            code_cel = nb.cells[2]
            if code_cel.cell_type == 'code':
                code_lines = code_cel.source.splitlines(keepends=True)
            else:
                code_lines = []

        return code_lines
    
    def get_correct_tests(self, results):
      return sum(1 for v in results.values() if v['correct'])

    def get_ui(self):
        self.render_text()

        return widgets.VBox([
            self.output,
            self.editor,
            self.submit_button,
            self.run_output
        ])

    def render_text(self):
        self.output.clear_output()
        with self.output:
            print(self.data.get("title", "No title"))
            print("-" * 40)
            print(self.data.get("text", ""))

    def check_answer(self, code_lines):
        code_str = "\n".join(code_lines)

        try:
            local_env = {}
            exec(code_str, {}, local_env)
        except Exception as e:
            return f"Compile/runtime error: {e}", False

        if "result" not in local_env:
            return "Error: 'result' not defined", False

        student_result = local_env["result"]

        if not isinstance(student_result, dict):
            return "Error: result must be a dictionary", False

        test_result = {}

        for key, expected_value in self.data.get("tests", {}).items():
            student_value = student_result.get(key, None)

            test_result[key] = {
                "result": "Correct" if str(student_value) == str(expected_value) else "Incorrect",
                "expected": expected_value,
                "student": student_value,
                "correct": str(student_value) == str(expected_value),
                "name": key
            }
        
        all_passed = True
        output_lines = []

        for name, info in test_result.items():
            if info["correct"]:
                output_lines.append(f"{name}: passed")
            else:
                output_lines.append(f"{name}: not passed")
                all_passed = False

        return "\n".join(output_lines), all_passed

    def submit(self, _):
        code = self.get_codecell()
        message, correct = self.check_answer(code)
        code_str = "\n".join(code)
        if correct:
            correct_str = 'correct'
        else:
            correct_str = 'incorrect' 
        self.controller.questionController.save_answer(self.data.get("title", "No title"),code_str, correct_str)
        self.run_output.clear_output()
        with self.run_output:
            print("Execution finished")
            print(message)
