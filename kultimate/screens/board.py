from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header

from ..widgets import BoardContainer


class KanbanBoard(Screen):
    """Screen for Boards"""

    TITLE = "Estamos en la pantalla Tablero"
    SUB_TITLE = "Sí, estamos en la pantalla tablero"
    BINDINGS = [
        ("ctrl+q", "app.pop_screen()", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield BoardContainer(id="board_container")
