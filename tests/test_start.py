import gc
import importlib.util
import os
import sqlite3
import subprocess
import sys
import warnings
from contextlib import closing

import pytest

from conftest import ROOT
from DB import DB


def load_start_module():
    # app.Start という名前で import するとゲームが始まるので、別名で読み込みます。
    spec = importlib.util.spec_from_file_location("StartUnderTest", ROOT / "app" / "Start.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def names_in_db():
    with closing(sqlite3.connect(DB.dbPath)) as connection:
        return {row[0] for row in connection.execute("SELECT name FROM saves")}


@pytest.mark.parametrize("key", ["make a,b", "make ", "make make foo"])
def test_invalid_names_are_not_created(db, monkeypatch, key):
    keys = iter([key])
    monkeypatch.setattr("builtins.input", lambda: next(keys))
    with pytest.raises(StopIteration):
        load_start_module().Start().start()
    assert names_in_db() == {"wada", "midori"}


def test_duplicate_name_closes_connection(db):
    gc.collect()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert DB.makeData("wada") is False
        gc.collect()
    assert not [w for w in caught if issubclass(w.category, ResourceWarning)]


def test_end_of_input_exits_quietly(db):
    result = subprocess.run(
        [sys.executable, "KillBirds.py"], cwd=ROOT, input="nobody\n",
        capture_output=True, text=True, timeout=60,
        env={**os.environ, "ISSEKI_DB": str(db)},
    )
    assert "データが見つかりませんでした" in result.stdout
    assert "Traceback" not in result.stderr
    assert result.returncode == 0
