import random
import re

import pytest

from CreateStone import CreateStone


def names(field):
    return {CreateStone.stones[key]["name"] for key in getattr(CreateStone, field + "Stones")}


@pytest.mark.parametrize("field", ["Nagoya", "Nagakute"])
def test_stone_comes_from_field_with_valid_size(field):
    random.seed(0)
    for _ in range(500):
        name, size = CreateStone.createStone(field).split("@")
        assert name in names(field)
        assert re.fullmatch(r"[0-5]\.[0-9]CM", size)
        assert 0.1 <= float(size[:-2]) <= 5.0
