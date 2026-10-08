from types import SimpleNamespace

import pytest

from CollectionBook import CollectionBook
from DB import DB


def pages(size):
    return [{"column%d" % (i + 1): size for i in range(10)} for _ in range(2)]


def test_full_book_of_largest_stones_scores_19000(monkeypatch):
    monkeypatch.setattr(DB, "loadPages4Score", lambda data: pages("5.0CM"))
    book = CollectionBook()
    assert book.checkComplete(SimpleNamespace()) is True
    assert book.calcScore(SimpleNamespace()) == 19000


def test_book_with_empty_column_is_not_complete(monkeypatch):
    rows = pages("1.0CM")
    rows[1]["column10"] = ""
    monkeypatch.setattr(DB, "loadPages4Score", lambda data: rows)
    assert CollectionBook().checkComplete(SimpleNamespace()) is False


def test_collect_stone_with_empty_bag_does_not_crash():
    data = SimpleNamespace(attr="browseStones4Collect", stonesList=[], cursor=0)
    data = CollectionBook().collectStone(data)
    assert data.attr == "browseStones4Collect"


def test_collecting_last_stone_keeps_cursor_in_bag(db):
    DB.makeData("tester")
    data = DB.load("tester")
    DB.addPage(data)
    data.stonesList = ["ラポ@2.0CM", "テンラグ@1.0CM"]
    data.cursor = 1
    data = CollectionBook().collectStone(data)
    assert data.stonesList == ["ラポ@2.0CM"]
    assert data.cursor == 0


@pytest.mark.parametrize("key", ["²", "99999999999999999999"])
def test_odd_page_numbers_are_rejected(db, monkeypatch, key):
    DB.makeData("tester")
    data = DB.load("tester")
    keys = iter([key, "x"])
    monkeypatch.setattr("builtins.input", lambda: next(keys))
    data = CollectionBook().openBook(data)
    assert data.m == -1


def test_perfect_clear_awards_trophy_and_completes_game(db, monkeypatch, capsys):
    DB.makeData("tester")
    data = DB.load("tester")
    DB.addPage(data)
    data.tmpScore = 19000
    data.trophiesList = ["ボス殲滅完了"]
    monkeypatch.setattr("builtins.input", lambda: "z")
    data = CollectionBook().clear(data)
    assert data.trophiesList == ["ボス殲滅完了", "クリアー", "極めクリアー"]
    assert data.scoreList[0].startswith("19000|")
    assert "You completed the Game!" in capsys.readouterr().out
    assert DB.load("tester").trophiesList == ["ボス殲滅完了", "クリアー", "極めクリアー"]
