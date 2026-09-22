import ipywidgets as widgets

class ProgrammingQuestion:
    def __init__(self, data, controller):
        self.data = data
        self.controller = controller
        self.output = widgets.Output(layout=widgets.Layout(width="100%"))

        self.editor = widgets.Textarea(
            layout=widgets.Layout(display='none')
        )

        self.submit_button = widgets.Button(
            description="Submit",
            button_style="primary",
            icon="check"
        )
        self.submit_button.on_click(self.submit)

        self.run_output = widgets.Output()
        self.answer_output = widgets.Output(layout=widgets.Layout(width="100%"))

        self.render_text()

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
        return widgets.VBox([
            self.output,
            self.editor,
            self.submit_button,
            self.run_output,
            self.answer_output
        ])

    def render_text(self):
        self.output.clear_output()
        with self.output:
            from IPython.display import display, HTML
            display(HTML(f"""
                <b>{self.data.get("title", "No title")}</b>
                <hr>
                <p style="white-space: pre-wrap; font-family: monospace;">{self.data.get("text", "")}</p>
            """))

    def check_answer(self, code_lines):
        tests = self.data.get("tests", {})
        if not tests:
            return "", True

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

        all_passed = True
        output_lines = []
        for key, expected_value in tests.items():
            student_value = student_result.get(key, None)
            correct = str(student_value) == str(expected_value)
            output_lines.append(f"{key}: {'passed' if correct else 'not passed'}")
            if not correct:
                all_passed = False

        return "\n".join(output_lines), all_passed

    def submit(self, _):
        code = self.get_codecell()
        message, correct = self.check_answer(code)
        code_str = "\n".join(code)
        correct_str = 'correct' if correct else 'incorrect'
        self.controller.questionController.save_answer(self.data.get("title", "No title"), code_str, correct_str)

        self.run_output.clear_output()
        with self.run_output:
            print("Submitted.")
            if message:
                print(message)

        model_answer = self.data.get("answer", None)
        self.answer_output.clear_output()
        if model_answer:
            with self.answer_output:
                from IPython.display import display, HTML
                display(HTML(f"""
                    <div style="background:#f0f7ff; border-left:4px solid #2196F3; padding:10px; margin-top:10px;">
                        <b>Model answer:</b><br>
                        <p style="white-space: pre-wrap; font-family: monospace;">{model_answer}</p>
                    </div>
                """))