import pytest

from kultimate.utils import ParserMarkdown


@pytest.fixture
def processMarkdown():
    return ParserMarkdown("/home/felipe/Dropbox/kanban2/todo.md")


def test_get_title(processMarkdown):
    """Obtiene el título h1 del archivo"""
    title = processMarkdown.get_title()
    assert title == "El título del documento"


def test_get_description(processMarkdown):
    """Obtiene la descripción del documento"""
    description = processMarkdown.get_description()
    assert (
        description
        == "Esta es la primera descripción\n\nEsta es la segunda descripción"
    )
