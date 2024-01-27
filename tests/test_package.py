import re


def test_import() -> None:
    from nexusravenv2utils import __version__

    assert isinstance(__version__, str)
    assert len(__version__) > 0
    assert re.match(r"^\d+\.\d+\.\d+$", __version__) is not None
