import ipywidgets as widgets
from IPython.display import display
from SelectComponent import SelectComponent
from SelectRun import SelectRun
from Overview import Overview

class Controller:
    def __init__(self, drive, online_version):
        self.component = None
        self.run = None
        self.drive = drive
        self.online_version = online_version
        self.selectComponent = SelectComponent(self)
        self.selectRun = SelectRun(self)
        self.overview = Overview(self)
        self.ui = widgets.VBox([
            self.selectComponent.get_ui(),
            self.selectRun.get_ui(),
            self.overview.get_ui()
        ])

    def start(self):
        display(self.ui)

    def show_run_selection(self):
        self.selectRun.set_runs(self.component)
        self.selectRun.show()

    def start_quiz(self):
        self.overview.refresh()