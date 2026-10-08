from types import SimpleNamespace

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
