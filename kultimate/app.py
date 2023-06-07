from pathlib import Path

from textual.app import App, ComposeResult
from textual.reactive import reactive, var
from textual.widgets import Footer, Header

from .utils import ParserMarkdown
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
    actual_file = var("")

    def __init__(self, path: str) -> None:
        """init kultimate"""
        self.home_directory = path
        self.SUB_TITLE = path
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        with StagesContainer():
            yield Directory(self.home_directory)
        yield Footer()

    # observar la variable self.actual_file
    def watch_actual_file(self) -> None:
        """Watch self.actual_file"""
        self.SUB_TITLE = self.actual_file
        self.refresh()

    def get_total_stages(self) -> None:
        try:
            self.list_stages = self.query(Stage)
            self.list_stages.first().focus()
            self.total_stages = len(self.list_stages) - 1
            self.stages_container = self.query(StagesContainer).first()
        except:
            pass

    async def on_key(self) -> None:
        await self.mount(StagesContainer())
        self.get_total_stages()

    def set_title(self, title: str, sub_title: str = "") -> None:
        """Change TITLE and SUB_TITLE"""
        self.TITLE = title
        self.SUB_TITLE = sub_title

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

    def unmount_stages(self) -> None:
        """Desmonta las columnas"""
        # TODO: Desmontar las columnas actuales - usar remove
        try:
            stages = self.query(Stage)
            for stage in stages:
                stage.remove()
        except:
            pass

    def mount_stages(self) -> None:
        """Monta las columnas"""
        # TODO: Montar las nuevas columnas usar mount
        try:
            stages_container = self.query(StagesContainer)[0]
            for stage in self.parser_content.get_stages():
                new_stage = Stage()
                new_stage.set_title(stage.text)
                stages_container.mount(new_stage)
                new_stage.scroll_visible()
            self.get_total_stages()
        except:
            with open("/home/felipe/Dropbox/kanban2/nel.txt", "w") as ff:
                ff.write("nel")

    # DONE: Seleccionar un archivo para mostrar.
    #### File selected
    def on_directory_tree_file_selected(self, event: Directory.FileSelected) -> None:
        event.stop()
        self.actual_file = str(event.path)
        # Ocultar Directory
        self.parser_content = ParserMarkdown(self.actual_file)
        self.action_select_file()
        self.unmount_stages()
        self.mount_stages()


def main(path: str) -> None:
    KULTIMATE(path).run()
