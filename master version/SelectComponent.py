import ipywidgets as widgets
from IPython.display import display
import os
import json

class SelectComponent:
    def __init__(self, controller):
        self.controller = controller
        
        self.start_button = widgets.Button(
            description="Start",
            button_style="success", 
            icon="play"
        )

        self.new_component_input = widgets.Text(
            description="Name:"
        )

        self.confirm_create_button = widgets.Button(
            description="Create",
            button_style="success",
            icon="check"
        )

        self.confirm_create_button.on_click(self.create_new_component)

        self.create_box = widgets.VBox([
            self.new_component_input,
            self.confirm_create_button
        ])

        self.create_box.layout.display = "none"

        self.new_component_button = widgets.Button(
            description="New component",
            button_style="warning", 
            icon="plus"
        )
        self.new_component_button.on_click(self.new_component)
        self.start_button.on_click(self.start)
        self.components = set()
        self.set_components()
        self.component_list = widgets.Dropdown(
            options=list(self.components),
            description="Component:"
        )
        
        self.vbox = widgets.VBox([
            self.component_list,
            self.create_box,
            widgets.HBox([self.new_component_button, self.start_button])
        ])

    def get_ui(self):
        return self.vbox
    
    def hide(self):
        self.component_list.layout.display = "none"
        self.start_button.layout.display = "none"
        self.new_component_button.layout.display = "none"
    
    def new_component(self, _):
        self.component_list.layout.display = "none"
        self.create_box.layout.display = ""

    def create_new_component(self, _):
        name = self.new_component_input.value.strip()

        if not name:
            print("Name cannot be empty")
            return
        
        self.components.add(name)
        self.component_list.options = sorted(self.components)

        self.new_component_input.value = ""
        self.create_box.layout.display = "none"
        self.component_list.layout.display = ""
        

    def set_components(self):
        for filename in os.listdir("../questions"):
            with open(f"../questions/{filename}", encoding="utf-8") as f:
                self.components.add(json.load(f)["component"])
        
    
    def start(self, value):
        self.controller.component = self.component_list.value
        self.hide()
        self.controller.show_run_selection()
