"""セーブデータの field 列はコードとして評価されてはいけません。"""
import random
from types import SimpleNamespace

import pytest

from CreateStone import CreateStone
from FieldJunction import FieldJunction
from RandomEvents import RandomEvents

INJECTED = "NagoyaStones if __import__('pytest').fail('field was evaluated') else Nagoya"


def test_field_junction_does_not_evaluate_field():
    data = SimpleNamespace(m=1, field=INJECTED)
    with pytest.raises(KeyError):
        FieldJunction.fieldJunction(data)


def test_create_stone_does_not_evaluate_field():
    with pytest.raises(AttributeError):
        CreateStone.createStone(INJECTED)


def test_random_event_does_not_evaluate_field(monkeypatch):
    monkeypatch.setattr(random, "randint", lambda a, b: 1)
    data = SimpleNamespace(field=INJECTED)
    with pytest.raises(AttributeError):
        RandomEvents().randomEvent(data)
