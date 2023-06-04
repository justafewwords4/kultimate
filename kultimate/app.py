from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header

from .widgets import Directory


class KULTIMATE(App):
    """The main app class"""

    TITLE = "KUltimate"
    SUB_TITLE = "Using Kanban with Markdown"
    CSS_PATH = "app.css"

    BINDINGS = [
        ("s", "select_file", "Select File"),
        ("q", "quit", "Quit"),
    ]

    home_user = Path.home()
    home_directory = "Dropbox/kanban2"

    def set_title(self, title: str, sub_title: str = "") -> None:
        """Change TITLE and SUB_TITLE"""
        self.TITLE = title
        self.SUB_TITLE = sub_title

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Directory(f"{self.home_user}/{self.home_directory}")
        yield Footer()

    def action_select_file(self) -> None:
        """Toggle class for Directory"""
        directory = self.query_one(Directory)
        directory.toggle_class("_visible")


def main() -> None:
    KULTIMATE().run()
