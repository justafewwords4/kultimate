######## Textual imports ######
from textual.app import App

from .screens import KanbanBoard, Main, SelectFile


###### Main Class ########
class KULTIMATE(App):
    """The main app class"""

    TITLE = "KUltimate"
    SUB_TITLE = "Using Kanban with Markdown"

    SCREENS = {
        "main": Main,
        "file": SelectFile,
        "board": KanbanBoard,
    }

    CSS_PATH = "app.css"

    def on_mount(self) -> None:
        """Mount Main screen"""
        self.push_screen("main")


def main() -> None:
    KULTIMATE().run()
