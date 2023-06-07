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


def test_get_stages(processMarkdown):
    """Obtiene las columnas del archivo"""
    h2s = processMarkdown.get_stages()
    assert len(h2s) == 5


def test_get_stages_names(processMarkdown):
    """Obtiene las columnas del archivo"""
    h2s = processMarkdown.get_stages()
    assert h2s[0].text == "Log" and h2s[1].text == "ToDo"
