import json
import pathlib

import pytest


@pytest.fixture
def json_file():
    """
    Allows for easily loading JSON fixtures from files
    """

    def loader(filename):
        with open(pathlib.Path(__file__).parent / "data" / f"{filename}.json") as fh:
            return json.load(fh)

    return loader
