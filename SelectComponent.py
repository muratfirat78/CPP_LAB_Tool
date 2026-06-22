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
        self.start_button.on_click(self.start)
        self.components = set()
        self.set_components()
        self.component_list = widgets.Dropdown(
            options=list(self.components),
            description="Component:"
        )
        
        self.vbox = widgets.VBox([self.component_list, self.start_button])

    def get_ui(self):
        return self.vbox
    
    def hide(self):
        self.component_list.layout.display = "none"
        self.start_button.layout.display = "none"



    def set_components(self):
        for filename in os.listdir("./questions"):
            with open(f"./questions/{filename}", encoding="utf-8") as f:
                self.components.add(json.load(f)["component"])
        
    
    def start(self, value):
        self.controller.component = self.component_list.value
        self.hide()
        self.controller.show_run_selection()