from textual.binding import Binding
from textual.widgets import DirectoryTree

# DONE: Aparecer y desaparecer el elemento Directory
# DONE: Perder el foco cuando se oculte el widget


class Directory(DirectoryTree):
    """Wrap DirectoryTree"""

    BINDINGS = [
        Binding("j", "cursor_down", "", False),
        Binding("k", "cursor_up", "", False),
        Binding("l", "cursor_select", "", False),
    ]
