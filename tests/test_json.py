import pathlib

import pytest

from .helpers import fail_unless_eval, get_test_data

paths = pathlib.Path("tests/json").rglob("*.json")


# TODO: The JSON tests never executed in the old test harness.
#       Now that they are running, it is clear they never actually worked.
#       They must be fixed!
@pytest.mark.xfail
@pytest.mark.parametrize("path", paths)
def test_json(path):
    text = path.read_text()
    description, eval_string, skip_unless = get_test_data(str(path), text)
    fail_unless_eval(str(path), eval_string)
