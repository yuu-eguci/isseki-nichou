import sqlite3

from DB import DB


def test_existing_saves_load(db):
    for name in ["wada", "midori"]:
        data = DB.load(name)
        assert data.name == name
        assert data.field in ["Nagoya", "Nagakute"]


def test_unknown_name_returns_false(db):
    assert DB.load("nobody") is False


def test_make_data_uses_defaults_and_rejects_duplicates(db):
    assert DB.makeData("tester") is True
    assert DB.makeData("tester") is False
    data = DB.load("tester")
    assert (data.field, data.m, data.gold) == ("Nagoya", 1, 1000)
    assert data.bulletsList == ["赤弾@50", "青弾@50", "黒弾@50"]
    assert data.stonesList == ["クズ石@1.0CM"]


def test_save_round_trip(db):
    DB.makeData("tester")
    data = DB.load("tester")
    data.m = 12
    data.gold = 345
    data.stonesList.append("ラポ@2.5CM")
    data.trophiesList.append("クリアー")
    DB.save(data)

    loaded = DB.load("tester")
    assert (loaded.m, loaded.gold) == (12, 345)
    assert loaded.stonesList == ["クズ石@1.0CM", "ラポ@2.5CM"]
    assert loaded.trophiesList == ["クリアー"]


def test_book_pages(db):
    DB.makeData("tester")
    data = DB.load("tester")
    assert DB.addPage(data) == 2
    assert DB.addPage(data) == 0

    data.target = "ラポ 2.5CM"
    assert DB.putInBook(data) is False
    data.target = "ラポ 3.0CM"
    assert DB.putInBook(data) == "2.5CM"
    data.page = 1
    assert DB.loadPage(data)["column6"] == "3.0CM"

    DB.resetBook(data)
    assert DB.loadPage(data)["column6"] == ""


def test_writes_go_to_db_path(db):
    DB.makeData("tester")
    with sqlite3.connect(db) as connection:
        rows = connection.execute("SELECT name FROM saves WHERE name='tester'").fetchall()
    assert rows == [("tester",)]
