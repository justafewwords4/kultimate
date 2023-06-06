from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from .widgets import Directory, Stage, StagesContainer


class KULTIMATE(App):
    """The main app class"""

    TITLE = "KUltimate"
    SUB_TITLE = "Using Kanban with Markdown"
    CSS_PATH = "app.css"

    BINDINGS = [
        ("s", "select_file", "Select File"),
        ("q", "quit", "Quit"),
        ("l, right", "go_to_right"),
        ("h, left", "go_to_left"),
    ]

    home_user = Path.home()
    # home_directory = "Dropbox/kanban2"
    is_directory_visible = False
    total_stages = 0
    actual_stage = 0
    actual_class = "_actual"
    actual_file = ""

    def __init__(self, path: str) -> None:
        """init kultimate"""
        self.home_directory = path
        self.SUB_TITLE = path
        super().__init__()

    async def on_key(self) -> None:
        await self.mount(StagesContainer())
        self.list_stages = self.query(Stage)
        self.list_stages.first().focus()
        self.total_stages = len(self.list_stages) - 1
        self.stages_container = self.query(StagesContainer).first()

    def set_title(self, title: str, sub_title: str = "") -> None:
        """Change TITLE and SUB_TITLE"""
        self.TITLE = title
        self.SUB_TITLE = sub_title

    def compose(self) -> ComposeResult:
        first = Stage(classes=self.actual_class)
        yield Header()
        with StagesContainer():
            yield Directory(self.home_directory)
            yield first
            yield Stage()
            yield Stage()
            yield Stage()
            yield Stage()
            yield Stage()
            yield Stage()
            yield Stage()
        yield Footer()

    def action_select_file(self) -> None:
        """Toggle class for Directory"""
        directory = self.query_one(Directory)
        directory.toggle_class("_visible")
        self.is_directory_visible = not self.is_directory_visible
        if self.is_directory_visible:
            self.set_focus(directory)
        else:
            self.set_focus(None)

    def scroll_and_focus(self) -> None:
        """Move scroll and focus a stage"""
        # DONE: Cambiar el foco al stage seleccionado
        self.stages_container.scroll_to_widget(self.list_stages[self.actual_stage])
        self.list_stages[self.actual_stage].focus()

    def action_go_to_right(self) -> None:
        """Go right"""
        self.list_stages[self.actual_stage].remove_class(self.actual_class)
        if self.actual_stage < self.total_stages:
            self.actual_stage += 1
        else:
            self.actual_stage = 0
        self.list_stages[self.actual_stage].add_class(self.actual_class)

        self.scroll_and_focus()

    def action_go_to_left(self) -> None:
        """Go left"""
        self.list_stages[self.actual_stage].remove_class(self.actual_class)
        if self.actual_stage > 0:
            self.actual_stage -= 1
        else:
            self.actual_stage = self.total_stages

        self.list_stages[self.actual_stage].add_class(self.actual_class)

        self.scroll_and_focus()

    #### File selected
    def on_directory_tree_file_selected(self, event: Directory.FileSelected) -> None:
        event.stop()
        self.actual_file = str(event.path)


def main(path: str) -> None:
    KULTIMATE(path).run()
