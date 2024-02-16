from builtins import ExceptionGroup
import main
import pytest

def test_answer():
    with pytest.raises(ExceptionGroup) as excinfo:
        data = main.main("/home/techytrickster/jupyter-tests/Dracula.txt")