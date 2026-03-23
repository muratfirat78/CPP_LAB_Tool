from ipywidgets import *
import json
import os

class QuestionEditor:
    def __init__(self, quiz):
        self.quiz = quiz
        self.tests_box = None
        self.save_button = Button(
            description="Save",
            button_style="success",
            icon="save"
        )

        self.delete_button = Button(
            description="Remove question",
            button_style="danger",
            icon="trash"
        )
        self.delete_button.on_click(self.delete_question)

        self.save_button.on_click(self.save_question)

        self.question_list_box = Select(
            options=self.quiz.questionsList.get_question_titles(),
            layout=Layout(width='150px', height='300px')
        )
        self.question_list_box.observe(self.select_question)
        
        self.title_input = Text(description="Title:")
        self.text_input = Textarea(description="Text:", layout=Layout(width="400px", height="100px"))
        self.index = Text(description="Index:")
        self.component_input = Text(description="Component:")
        self.type_dropdown = Dropdown(
            options=['open', 'multiple_choice', 'programming', 'custom', 'info'],
            description='Type:'
        )
        
        self.type_specific_output = VBox()
        
        self.editor_box = VBox([
            self.title_input,
            self.text_input,
            self.index,
            self.component_input,
            self.type_dropdown,
            self.type_specific_output,
            HBox([self.save_button, self.delete_button])
        ])
        
        self.main_ui = HBox([
            self.question_list_box,
            self.editor_box
        ])
        
        self.type_dropdown.observe(self.update_type_specific_area, names='value')
    
    def select_question(self, change):
        question = self.quiz.questionsList.get_question(self.question_list_box.value)
        self.title_input.value = question.get("title")
        self.text_input.value = question.get("text")
        self.index.value = str(question.get("index"))
        self.component_input.value = question.get("component")
        self.type_dropdown.value = question.get("type")
        self.update_type_specific_area({"new": question.get("type")})

    def update_type_specific_area(self, change):
        qtype = change['new']
        self.type_specific_output.children = []
        
        if qtype == 'open':
            self.type_specific_output.children = [self.get_open_question_editor()]
        elif qtype == 'multiple_choice':
            self.type_specific_output.children = [self.get_multiple_choice_editor()]
        elif qtype == 'programming':
            self.type_specific_output.children = [self.get_programming_editor()]
        elif qtype == 'info':
            self.type_specific_output.children = [self.get_info_editor()]
        else:
            self.type_specific_output.children = [self.get_custom_editor()]

    def get_open_question_editor(self):
        question = self.quiz.questionsList.get_question(self.question_list_box.value)
        correct_answer = Text(description="Answer:")
        correct_answer.value = question.get("correctness")
        return correct_answer
    

    def get_multiple_choice_editor(self):
        question = self.quiz.questionsList.get_question(self.question_list_box.value)

        options = question.get("choices", [])
        correctness = question.get("correctness", [])

        self.options_box = VBox()

        def create_option_row(text="", correct=False):
            option_text = Text(value=text, description="Option:")
            option_correct = Checkbox(value=correct, description="Correct")
            remove_button = Button(description="Remove", button_style="danger")

            row = HBox([option_text, option_correct, remove_button])

            def remove_option(_):
                self.options_box.children = tuple(
                    child for child in self.options_box.children if child is not row
                )

            remove_button.on_click(remove_option)

            return row

        rows = []
        for i, option in enumerate(options):
            rows.append(create_option_row(option, correctness[i]))

        self.options_box.children = tuple(rows)

        add_button = Button(description="Add option", button_style="success")

        def add_option(_):
            new_row = create_option_row("", False)
            self.options_box.children = self.options_box.children + (new_row,)

        add_button.on_click(add_option)

        return VBox([self.options_box, add_button])
        
    def get_programming_editor(self):
        question = self.quiz.questionsList.get_question(self.question_list_box.value)

        keywords = question.get("correctness", {}).get("keywords", [])
        keywords_box = Text(value=",".join(keywords), description="Keywords:")

        solution_lines = question.get("correctness", {}).get("solution", [])
        solution_box = Textarea(value="\n".join(solution_lines), description="Solution", layout={"width": "600px", "height": "150px"})

        tests = question.get("correctness", {}).get("tests", [])
        self.tests_box = VBox()

        def create_test_row(test):
            name = Text(value=test.get("name", ""), description="Test Name:")
            expected = Text(value=str(test.get("expected", "")), description="Expected:")

            options = ['return', 'output', 'class_method', 'inheritance']
            test_type = Dropdown(
                options=options,
                value=test.get("type") if test.get("type") in options else options[0],
                description='Type:'
            )

            if test_type.value in ['return', 'class_method', 'output']:
                expected = Text(value=str(test.get("expected", "")), description="Expected:")
            else:
                expected = None
         
            if test_type.value in ['return', 'class_method']:
                input_val = Text(value=str(test.get("input", "")), description="Input:")  
            else:
                input_val = None
            
            if test_type.value in ['class_method','inheritance']:
                class_name_box = Text(value=test.get("class_name", ""), description="Class Name:") 
            else:
                class_name_box = None

            if test_type.value == 'class_method':
                function_name = Text(value=test.get("method", ""), description="Function:")
            else:
                function_name = None

            if test_type.value == 'inheritance':
                parent_class = Text(value=test.get("parent_class", ""), description="Parent class:")
            else:
                parent_class = None

            remove_button = Button(description="Remove", button_style="danger")

            # Create the row layout dynamically
            row_children = [name]
            for widget in [function_name, input_val, class_name_box, parent_class, expected, test_type, remove_button]:
                if widget is not None:
                    row_children.append(widget)
            row = VBox([
                VBox(row_children),
                Label("_______________________________________________")
            ])

            def remove_test(_):
                self.tests_box.children = tuple(c for c in self.tests_box.children if c is not row)

            def on_type_change(change):
                new_type = change['new']
                nonlocal row_children, input_val, class_name_box, function_name, parent_class, expected
                row_children = [name] 

                #update values
                input_val = Text(value=str(test.get("input", "")), description="Input:") if new_type in ['return', 'class_method'] else None
                class_name_box = Text(value=test.get("class_name", ""), description="Class Name:") if new_type == 'class_method' else None
                function_name = Text(value=test.get("method", ""), description="Method:") if new_type in ['class_method'] else None
                parent_class = Text(value=test.get("parent_class", ""), description="Parent class:") if new_type == 'inheritance' else None
                expected = Text(value=str(test.get("expected", "")), description="Expected:") if new_type in ['return', 'output', 'class_method'] else None
                
                for widget in [function_name, input_val, class_name_box, parent_class, expected, test_type, remove_button]:
                    if widget is not None:
                        row_children.append(widget)
                row.children = row_children

            test_type.observe(on_type_change, names='value')
            remove_button.on_click(remove_test)
            return row

        tests_rows = [create_test_row(t) for t in tests]
        self.tests_box.children = tuple(tests_rows)

        add_test_button = Button(description="Add Test", button_style="warning")

        def add_test(_):
            new_test = create_test_row({"name": "", "input": "", "expected": "", "type": ""})
            self.tests_box.children = self.tests_box.children + (new_test,)
            

        add_test_button.on_click(add_test)

        editor = VBox([ keywords_box, solution_box,Label("_______________________________________________"),self.tests_box, add_test_button])
        return editor
    
    def get_info_editor(self):
        return Text(description="info")
    
    def get_custom_editor(self):
        return Text(description="custom")
        
    def get_QuestionEditor(self):
        return self.main_ui
    
    def get_tests_data(self):
        tests = []
        for row in self.tests_box.children:
            widgets = row.children[0].children  
            test_data = {}

            for w in widgets:
                if isinstance(w, Text):
                    if w.description == "Test Name:":
                        test_data["name"] = w.value
                    elif w.description == "Input:":
                        test_data["input"] = w.value
                    elif w.description == "Expected:":
                        test_data["expected"] = w.value
                    elif w.description == "Class Name:":
                        test_data["class_name"] = w.value
                    elif w.description == "Function:":
                        test_data["method"] = w.value
                    elif w.description == "Parent class:":
                        test_data["parent_class"] = w.value

                elif isinstance(w, Dropdown):
                    test_data["type"] = w.value
            modified_test = {}
            modified_test["name"] = test_data["name"]
            modified_test["type"] = test_data["type"]

            if test_data["type"] == 'return':
                modified_test["input"] = test_data["input"]
                modified_test["expected"] =  test_data["expected"]

            if test_data["type"] == 'output':
                modified_test["expected"] =  test_data["expected"]
            
            if test_data["type"] == 'class_method':
                modified_test["class_name"] = test_data["class_name"]
                modified_test["input"] =  test_data["expected"]
                modified_test["method"] =  test_data["method"]
                modified_test["expected"] = test_data["expected"]
        
            if test_data["type"] == 'inheritance':
                modified_test["class_name"] = test_data["class_name"]
                modified_test["parent_class"] =  test_data["parent_class"]

            tests.append(modified_test)
        return tests

    def get_multiple_choice_data(self):
        choices = []
        correctness = []

        for row in self.options_box.children:
            option_text, option_correct, _ = row.children
            choices.append(option_text.value)
            correctness.append(option_correct.value)

        return choices, correctness

    def delete_question(self,change):
        title = self.title_input.value
        filename = title.lower().replace(" ", "_") + ".json"

        filepath = os.path.join("questions", filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            
        self.question_list_box.unobserve(self.select_question)
        self.quiz.questionsList.remove_question(title)
        self.question_list_box.value = None
        self.question_list_box.options = self.quiz.questionsList.get_question_titles()
        self.question_list_box.observe(self.select_question)
        self.title_input.value = ""
        self.text_input.value = ""
        self.index.value = ""
        self.component_input.value = ""
        self.type_dropdown.value = None
        self.type_specific_output.children = []

    def save_question(self, change):
        question = {}
        question["title"] = self.title_input.value
        question["text"] = self.text_input.value
        question["index"] = int(self.index.value)
        question["component"] = self.component_input.value
        
        question["type"] = self.type_dropdown.value

        if self.type_dropdown.value == "programming":
            print(self.get_tests_data())
        
        if self.type_dropdown.value == 'multiple_choice':
            choices, correctness = self.get_multiple_choice_data()

            question["choices"] = choices
            question["correctness"] = correctness
        
        
        filename = question["title"].lower().replace(" ", "_") + ".json"
        filepath = os.path.join("questions", filename)

        with open(filepath, "w") as f:
            json.dump(question, f, indent=4)
        self.quiz.questionsList.update_question(question)
        self.question_list_box.options = self.quiz.questionsList.get_question_titles()