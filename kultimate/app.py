from pathlib import Path

from textual.app import App, ComposeResult
from textual.reactive import reactive, var
from textual.widgets import Footer, Header

from .utils import ParserMarkdown
from .widgets import Directory, Stage, StagesContainer

# DONE: Hay errores al navegar entre las columnas.


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
    current_stage = 0
    class_stage_is_visible = "_actual"
    actual_file = var("")

    def __init__(self, path: str) -> None:
        """init kultimate"""
        self.home_directory = path
        self.SUB_TITLE = path
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        with StagesContainer(id="stages_container"):
            yield Directory(self.home_directory, id="directory")
        yield Footer()

    # observar la variable self.actual_file
    def watch_actual_file(self) -> None:
        """Watch self.actual_file"""
        self.SUB_TITLE = self.actual_file
        self.refresh()

    def get_total_stages(self) -> None:
        try:
            self.list_stages = self.query(Stage)
            # self.list_stages.first().focus()
            self.list_stages.first().add_class(self.class_stage_is_visible)
            # Establece la primer columna como la actual
            self.current_stage = 0
            # self.list_stages.first().scroll_visible()
            self.total_stages = len(self.list_stages) - 1
            # self.stages_container = self.query("#stages_container").first()
            self.scroll_and_focus()
        except:
            pass

    async def on_key(self) -> None:
        await self.mount(StagesContainer())
        # self.get_total_stages()

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
        self.list_stages[self.current_stage].focus()
        self.list_stages[self.current_stage].scroll_visible()

    def write_right(self) -> None:
        with open("/home/felipe/Dropbox/kanban2/right.txt", "a") as ff:
            ff.write(f"{self.current_stage}\n")

    def action_go_to_right(self) -> None:
        """Go right stage"""

        self.list_stages[self.current_stage].remove_class(self.class_stage_is_visible)

        if self.current_stage < self.total_stages:
            self.current_stage += 1
        else:
            self.current_stage = 0

        self.list_stages[self.current_stage].add_class(self.class_stage_is_visible)

        self.scroll_and_focus()

    def action_go_to_left(self) -> None:
        """Go left stage"""
        self.list_stages[self.current_stage].remove_class(self.class_stage_is_visible)

        if self.current_stage > 0:
            self.current_stage -= 1
        else:
            self.current_stage = self.total_stages

        self.list_stages[self.current_stage].add_class(self.class_stage_is_visible)

        self.scroll_and_focus()

    def unmount_stages(self) -> None:
        """Desmonta las columnas"""
        # DONE: Desmontar las columnas actuales - usar remove
        try:
            stages = self.query(Stage)
            for stage in stages:
                stage.remove()
        except:
            pass

    def mount_stages(self) -> None:
        """Monta las columnas"""
        # DONE: Montar las nuevas columnas. Usar mount
        try:
            stages_container = self.query("#stages_container")[0]
            stages = self.parser_content.get_stages()
            for stage in stages:
                new_stage = Stage()
                new_stage.set_title(stage.text)
                stages_container.mount(new_stage)

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
