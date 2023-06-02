import pytest

from kultimate.utils import ProcessYaml


@pytest.fixture
def yaml():
    return ProcessYaml()


def test_valid_yaml(yaml):
    """Determina si el yaml es válido"""
    yaml.set_path("todo.yml")
    assert len(yaml.json_dir["stages"]) == 5
