from textual.binding import Binding
from textual.widgets import DirectoryTree


class Directory(DirectoryTree):
    """Wrap DirectoryTree"""

    BINDINGS = [
        Binding("j", "cursor_down", "", False),
        Binding("k", "cursor_up", "", False),
        Binding("l", "select_file", "", False),
        Binding("q", "app.pop_screen", "", False),
    ]

    def action_select_file(self) -> None:
        self.app.pop_screen()
