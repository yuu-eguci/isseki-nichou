import hashlib
import shutil
from pathlib import Path

import pytest

import CommonFunctions
import Screen
from DB import DB

ROOT = Path(__file__).resolve().parent.parent
COMMITTED_DBS = [ROOT / "app" / "isseki.sqlite3", ROOT / "app" / "common" / "isseki.sqlite3"]


def _digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope="session", autouse=True)
def committed_dbs_are_untouched():
    """コミット済みの DB をテストが書き換えていないことを確認します。"""
    before = {path: _digest(path) for path in COMMITTED_DBS}
    yield
    assert {path: _digest(path) for path in COMMITTED_DBS} == before


@pytest.fixture(autouse=True)
def fast_and_isolated(monkeypatch, tmp_path):
    """1 文字ずつの表示待ちを無くし、相対パスの DB に届かないようにします。"""
    monkeypatch.setattr(CommonFunctions, "messageInterval", 0)
    monkeypatch.chdir(tmp_path)
    Screen.reset()


@pytest.fixture
def db(monkeypatch, tmp_path):
    """コミット済み DB の使い捨てコピーを DB.dbPath に設定します。"""
    path = tmp_path / "isseki.sqlite3"
    shutil.copyfile(COMMITTED_DBS[0], path)
    monkeypatch.setattr(DB, "dbPath", str(path))
    return path
