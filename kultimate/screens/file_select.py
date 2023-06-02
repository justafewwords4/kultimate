from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen

from ..widgets import Directory

home = Path.home()


class SelectFile(Screen):
    """Push window to select a file"""

    # DONE: Revisar esta liga https://textual.textualize.io/guide/screens/#__tabbed_3_4

    def compose(self) -> ComposeResult:
        yield Grid(
            Directory(f"{home}/Dropbox/kanban2", id="question"),
            id="select_file",
        )
