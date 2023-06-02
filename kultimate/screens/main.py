from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header

# TODO: Ver si puedo usar yaml en lugar de markdown


class Main(Screen):
    """Main Screen of application"""

    DEFAULT_CSS = """
    Main {
        background: $primary-background-darken-1;
    }
    """

    BINDINGS = [
        ("s", "app.push_screen('file')", "Select File"),
        ("k", "app.push_screen('board')", "Kanban Board"),
        ("q", "app.quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
