from pathlib import Path

from textual.app import App, ComposeResult
from textual.reactive import var
from textual.widgets import Footer, Header

from .utils import ParserMarkdown
from .widgets import Directory, Stage, StagesContainer, Task

# DONE: Hay errores al navegar entre las columnas.

EXAMPLE_MARKDOWN = """\
# Markdown Document

This is an example of Textual's `Markdown` widget.

## Features

Markdown syntax and extensions are supported.

- Typography *emphasis*, **strong**, `inline code` etc.
- Headers
- Lists (bullet and ordered)
- Syntax highlighted code blocks
- Tables!
"""


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
    class_for_selected_stage = "_actual"
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
        self.sub_title = self.actual_file

    def get_total_stages(self) -> None:
        try:
            self.list_stages = self.query(Stage)
            self.list_stages.first().add_class(self.class_for_selected_stage)
            self.current_stage = 0
            self.total_stages = len(self.list_stages) - 1
            self.scroll_and_focus()
            # Borrar después
        except:
            pass

    async def on_key(self) -> None:
        try:
            stages_container = self.query_one(StagesContainer)
            if not stages_container:
                await self.mount(StagesContainer())
        except:
            pass
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
        self.query("#stages_container")[0].scroll_visible(
            self.list_stages[self.current_stage]
        )
        # self.list_stages[self.current_stage].scroll_visible()

    def write_right(self) -> None:
        """Función auxiliar"""
        with open("/home/felipe/Dropbox/kanban2/subtitle.txt", "a") as ff:
            ff.write(f"subtitle modificado {self.SUB_TITLE}\n")

    def action_go_to_right(self) -> None:
        """Go right stage"""

        if len(self.list_stages):
            self.list_stages[self.current_stage].remove_class(
                self.class_for_selected_stage
            )

            if self.current_stage < self.total_stages:
                self.current_stage += 1
            else:
                self.current_stage = 0

            self.list_stages[self.current_stage].add_class(
                self.class_for_selected_stage
            )

            self.scroll_and_focus()

    def action_go_to_left(self) -> None:
        """Go left stage"""

        if len(self.list_stages):
            self.list_stages[self.current_stage].remove_class(
                self.class_for_selected_stage
            )

            if self.current_stage > 0:
                self.current_stage -= 1
            else:
                self.current_stage = self.total_stages

            self.list_stages[self.current_stage].add_class(
                self.class_for_selected_stage
            )

            self.scroll_and_focus()

    def unmount_stages(self) -> None:
        """Desmonta las columnas"""
        # DONE: Desmontar las columnas actuales - usar remove
        try:
            stages = self.query(Stage)
            for stage in stages:
                stage.remove()
        except IndexError:
            pass

    def mount_stages(self) -> None:
        """Monta las columnas"""
        # DONE: Montar las nuevas columnas. Usar mount
        try:
            stages_container = self.query("#stages_container")[0]
            stages = self.parser_content.get_stages()
            # DONE: Montar tareas en las columnas
            for stage in stages:
                new_stage = Stage()
                new_stage.set_title(stage.text)
                # TODO: Que la primer tarea obtenga el foco
                # TODO: Moverse entre tareas con j y k
                # TODO: Mover tareas con J, K, H y L
                for n in range(3):
                    new_stage.mount(Task(EXAMPLE_MARKDOWN))
                stages_container.mount(new_stage)

            self.get_total_stages()

        except IndexError:
            with open("/home/felipe/Dropbox/kanban2/nel.txt", "w") as ff:
                ff.write("nel")

    # DONE: Seleccionar un archivo para mostrar.
    # File selected
    def on_directory_tree_file_selected(
        self,
        event: Directory.FileSelected,
    ) -> None:
        event.stop()
        self.actual_file = str(event.path)
        # Ocultar Directory
        self.parser_content = ParserMarkdown(self.actual_file)
        self.action_select_file()
        self.unmount_stages()
        self.mount_stages()
        self.refresh()


def main(path: str) -> None:
    KULTIMATE(path).run()
