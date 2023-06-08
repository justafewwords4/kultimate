from pathlib import Path

from textual.app import App, ComposeResult
from textual.css.query import QueryError
from textual.reactive import var
from textual.widgets import Footer, Header

from .utils import ParserMarkdown
from .widgets import Directory, Stage, StagesContainer, Task

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
        ("j, down", "go_to_down"),
        ("k, up", "go_to_up"),
    ]

    home_user = Path.home()
    # home_directory = "Dropbox/kanban2"
    is_directory_visible = False
    total_stages = 0
    current_stage = 0
    # Clases para la columna y la tarea activa
    class_for_selected_stage = "_actual"
    class_for_active_task = "_active"
    # Archivo md en el que se está trabajando
    actual_file = var("")
    # Variables para las tareas
    # poner a cero cuando se presione l o h
    current_task = 0
    total_tasks = 0

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
        # por alguna razón hay que poner sub_title en minúsculas, no en
        # mayúsculas, o no funciona
        self.sub_title = self.actual_file

    def get_total_stages(self) -> None:
        try:
            self.list_stages = self.query(Stage)
            self.list_stages.first().add_class(self.class_for_selected_stage)
            self.current_stage = 0
            self.total_stages = len(self.list_stages) - 1
            self.scroll_and_focus_stage()
            # Borrar después
        except QueryError:
            pass

    async def on_key(self) -> None:
        try:
            stages_container = self.query_one(StagesContainer)
            if not stages_container:
                await self.mount(StagesContainer())
        except QueryError:
            pass

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

    def scroll_and_focus_stage(self) -> None:
        """Move scroll and focus a stage"""
        # Esta es la función que se llama cuando se cambia de columna
        # DONE: Cambiar el foco al stage seleccionado
        self.list_stages[self.current_stage].focus()
        self.query("#stages_container")[0].scroll_visible(
            self.list_stages[self.current_stage]
        )
        # Hasta aquí las operaciones para la columna

        # Ahora las operaciones para las tareas
        # self.list_stages[self.current_stage].scroll_visible()

        # DONE: No he podido quitar la clase de la tarea en la columna anterior
        # Lo tengo que hacer antes de entrar a esta función, cuando presiono
        # las teclas h y l

        # DONE: Poner la columna actual a cero
        self.current_task = 0
        try:
            self.list_tasks = self.list_stages[self.current_stage].query(Task)
            # DONE: Obtener el total de tareas en la columna
            self.total_tasks = len(self.list_tasks) - 1
        except:
            self.total_tasks = 0
        if self.list_tasks:
            self.list_tasks[self.current_task].add_class(self.class_for_active_task)

    def scroll_and_focus_task(self) -> None:
        """Move scroll and focus a task"""
        # Esta es la función que se llama cuando se cambia de columna
        # DONE: Cambiar el foco al stage seleccionado
        if self.list_tasks:
            self.list_tasks[self.current_task].focus()
            self.list_tasks[self.current_task].scroll_visible()

    def write_right(self) -> None:
        """Función auxiliar"""
        with open("/home/felipe/Dropbox/kanban2/subtitle.txt", "a") as ff:
            ff.write(f"subtitle modificado {self.SUB_TITLE}\n")

    def eliminate_active_class_for_task(self):
        """Quitar la clase de tarea activa para la columna actual"""
        try:
            # Si existe una lista de tareas eliminar la clase de tarea activa
            self.list_tasks[self.current_task].remove_class(
                self.class_for_active_task,
            )
        except:
            pass

    def action_go_to_right(self) -> None:
        """Go right stage"""

        self.eliminate_active_class_for_task()

        self.current_task = 0
        self.total_tasks = 0

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

            self.scroll_and_focus_stage()
            self.scroll_and_focus_task()

    def action_go_to_left(self) -> None:
        """Go left stage"""

        self.eliminate_active_class_for_task()

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

            self.scroll_and_focus_stage()

    # DONE: Moverse entre tareas con j y k
    def action_go_to_down(self) -> None:
        """Ir a la tarea de abajo"""
        # ¿en qué columna estoy?
        # obtener la tarea activa: self.current_task es la tarea actual
        # quitar la clase de tarea activa
        if self.list_tasks:
            self.list_tasks[self.current_task].remove_class(self.class_for_active_task)
            # ir abajo
            if self.current_task < self.total_tasks:
                self.current_task += 1
            else:
                self.current_task = 0
            # poner clase de tarea activa
            self.list_tasks[self.current_task].add_class(self.class_for_active_task)

            self.scroll_and_focus_task()

    def action_go_to_up(self) -> None:
        """Ir a la tarea de arriba"""
        if self.list_tasks:
            self.list_tasks[self.current_task].remove_class(self.class_for_active_task)
            # ir arriba
            if self.current_task > 0:
                self.current_task -= 1
            else:
                self.current_task = self.total_tasks
            # poner clase de tarea activa
            self.list_tasks[self.current_task].add_class(self.class_for_active_task)

            self.scroll_and_focus_task()

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
            tasks = self.parser_content.get_tasks()
            # DONE: Montar tareas en las columnas
            for index, stage in enumerate(stages):
                new_stage = Stage()
                new_stage.set_title(stage.text)
                # TODO: Mover tareas con J, K, H y L
                first_task = True
                for task in tasks[index]:
                    new_task = Task(task)
                    new_stage.mount(new_task)
                    # DONE: Que la primer tarea obtenga el foco
                    if index == 0 and first_task:
                        new_task.focus()
                        first_task = False
                        new_task.add_class(self.class_for_active_task)

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
