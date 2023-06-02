from textual.app import App

from .screens import KanbanBoard, Main, SelectFile


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

    def set_title(self, title: str, sub_title: str = "") -> None:
        """Change TITLE and SUB_TITLE"""
        self.TITLE = title
        self.SUB_TITLE = sub_title


def main() -> None:
    KULTIMATE().run()
