"""画面の組み立て (ヘッダー・場面・出来事・キー) と、追記表示の挙動を確かめるテストです。"""
import re
from types import SimpleNamespace

import pytest

import Screen
from DB import DB
from KickEnemy import KickEnemy

ANSI = re.compile(r"\x1b")


def player(**overrides):
    data = SimpleNamespace(
        name="tester", field="Nagoya", m=12, gold=1000, stonesList=["ラポ@1.0CM", "クズ石@1.0CM"],
        gunsList=["汎用駆除銃@1"], bulletsList=["赤弾@50", "青弾@50", "黒弾@50"],
        scoreList=[], trophiesList=[], troDataList=[],
    )
    for key, value in overrides.items():
        setattr(data, key, value)
    return data


def keys_from(monkeypatch, *keys):
    feed = iter(keys)
    monkeypatch.setattr("builtins.input", lambda: next(feed))


def test_display_width_counts_japanese_as_two_columns():
    assert Screen.width("abc") == 3
    assert Screen.width("ナゴヤ") == 6


def test_wrap_respects_display_width():
    lines = Screen.wrap("あいうえおかきくけこ", 8)
    assert lines == ["あいうえ", "おかきく", "けこ"]


def test_keys_wrap_before_brackets_on_narrow_terminal():
    lines = Screen.wrapKeys("[w]進む [s]戻る [c]メニュー [save]セーブ [quit]終了", 20)
    assert lines == ["[w]進む [s]戻る", "[c]メニュー", "[save]セーブ", "[quit]終了"]


def test_narrow_frame_keeps_save_state_and_every_key():
    Screen.markSaved(player())
    lines = Screen.frame(["草木が微風にそよいでいる。"], [], "[w]進む [s]戻る [quit]終了", 16, 20)
    assert "保存済み" in "".join(lines)
    assert "[quit]終了" in lines
    assert all(Screen.width(line) <= 16 for line in lines)


def test_table_aligns_columns_and_marks_cursor():
    lines = Screen.table([["ラポ", "1.0CM"], ["エティルドナグゼラ", "5.0CM"]], 1)
    assert lines[0].startswith("  ラポ")
    assert lines[1].startswith("> エティルドナグゼラ")
    assert Screen.width(lines[0].split("1.0CM")[0]) == Screen.width(lines[1].split("5.0CM")[0])


def test_bar_shows_remaining_cells_and_numbers():
    assert Screen.bar(2, 3) == "[##.] 2/3"
    assert Screen.bar(-1, 3) == "[...] 0/3"


def test_header_shows_area_distance_gold_stones_and_save_state():
    data = player()
    Screen.markSaved(data)
    assert Screen.header() == "ナゴヤ・エリア 12 M | 所持金 1000 | 石 2 | 保存済み"
    data.m = -1
    assert Screen.header().startswith("キャンプ | ")


def test_cursor_and_menu_movement_do_not_make_unsaved():
    data = player()
    Screen.markSaved(data)
    data.cursor, data.attr = 2, "browseStones"
    assert not Screen.isDirty()
    data.m = 13
    assert Screen.isDirty()


def test_save_and_load_mark_saved(db):
    data = DB.load("wada")
    assert not Screen.isDirty()
    data.gold += 1
    assert Screen.isDirty()
    DB.save(data)
    assert not Screen.isDirty()


def test_frame_has_header_scene_log_and_keys_at_bottom():
    Screen.markSaved(player())
    lines = Screen.frame(["草木が微風にそよいでいる。"], ["1M進んだ。"], "[w]進む [s]戻る", 40, 12)
    assert lines[0].startswith("ナゴヤ・エリア 12 M")
    assert "草木が微風にそよいでいる。" in lines
    assert "1M進んだ。" in lines
    assert lines[-1] == "[w]進む [s]戻る"
    assert len(lines) <= 11
    assert all(Screen.width(line) <= 40 for line in lines)


def test_frame_keeps_newest_log_lines_on_short_terminal():
    log = ["出来事%d" % i for i in range(30)]
    lines = Screen.frame(["場面"], log, "[x]戻る", 40, 8)
    assert "出来事29" in lines
    assert "出来事0" not in lines
    assert len(lines) <= 7


def test_plain_output_has_no_ansi_or_system_prefix(monkeypatch, capsys):
    keys_from(monkeypatch, "w")
    Screen.markSaved(player())
    Screen.scene("草木が微風にそよいでいる。")
    Screen.say("1M進んだ。")
    assert Screen.ask("[w]進む") == "w"
    out = capsys.readouterr().out
    assert not ANSI.search(out)
    assert "<SYSTEM>" not in out
    assert "[w]進む" in out


def test_plain_output_does_not_repeat_unchanged_scene(monkeypatch, capsys):
    keys_from(monkeypatch, "w", "w")
    for _ in range(2):
        Screen.scene("草木が微風にそよいでいる。")
        Screen.ask("[w]進む")
    assert capsys.readouterr().out.count("草木が微風にそよいでいる。") == 1


def test_tty_repaints_once_per_input_without_clearing_whole_screen(monkeypatch, capsys):
    keys_from(monkeypatch, "w")
    monkeypatch.setattr(Screen, "isPlain", lambda: False)
    Screen.markSaved(player())
    Screen.scene("草木が微風にそよいでいる。")
    Screen.ask("[w]進む")
    out = capsys.readouterr().out
    assert out.count("\x1b[H") == 1
    assert "\x1b[2J" not in out
    assert "保存済み" in out


def test_quit_without_unsaved_progress_exits(monkeypatch):
    keys_from(monkeypatch, "quit")
    Screen.markSaved(player())
    with pytest.raises(SystemExit):
        Screen.ask("[w]進む", quit=True)


def test_quit_with_unsaved_progress_asks_and_can_cancel(monkeypatch, capsys):
    keys_from(monkeypatch, "quit", "x", "w")
    data = player()
    Screen.markSaved(data)
    data.m += 1
    assert Screen.ask("[w]進む", quit=True) == "w"
    assert "セーブしていない" in capsys.readouterr().out


def test_quit_with_unsaved_progress_exits_when_confirmed(monkeypatch):
    keys_from(monkeypatch, "quit", "z")
    data = player()
    Screen.markSaved(data)
    data.m += 1
    with pytest.raises(SystemExit):
        Screen.ask("[w]進む", quit=True)


def test_quit_is_ordinary_text_where_not_offered(monkeypatch):
    keys_from(monkeypatch, "quit")
    assert Screen.ask("[x]戻る") == "quit"


def test_battle_screen_shows_hp_bars_gun_and_ammo(monkeypatch, capsys):
    keys_from(monkeypatch, "z", "z")
    data = player(enemy="Alligator", m=5)
    KickEnemy().kickEnemy(data)
    out = capsys.readouterr().out
    assert "ワニ [###] 3/3" in out
    assert "自分 [###] 3/3" in out
    assert "汎用駆除銃" in out
    assert re.search(r"> 赤弾 +x50", out)
    assert "[w/s]弾を選ぶ [z]撃つ [x]諦める" in out


def test_collection_book_shows_count_of_twenty(db, monkeypatch, capsys):
    from CollectionBook import CollectionBook
    data = DB.load("wada")
    keys_from(monkeypatch, "x")
    data.m = -1
    CollectionBook().openBook(data)
    assert re.search(r"収集 \d+/20 種", capsys.readouterr().out)


def test_stone_bag_does_not_reveal_unappraised_stone(monkeypatch, capsys):
    from Inventory import Inventory
    keys_from(monkeypatch, "x")
    data = player(stonesList=["石@(未鑑定)@ターコイズ@3.5CM"])
    Inventory().browseStones(data)
    out = capsys.readouterr().out
    assert "(未鑑定)" in out
    assert "ターコイズ" not in out


def test_plain_output_shows_header_only_when_it_changes(monkeypatch, capsys):
    keys_from(monkeypatch, "c", "w", "w")
    data = player()
    Screen.markSaved(data)
    Screen.ask("[w]進む")
    Screen.ask("[w]進む")
    data.m += 1
    Screen.ask("[w]進む")
    out = capsys.readouterr().out
    assert out.count("ナゴヤ・エリア 12 M") == 1
    assert "-- ナゴヤ・エリア 13 M | 所持金 1000 | 石 2 | 未保存 --" in out


def test_repeated_message_is_counted_instead_of_filling_the_log(monkeypatch):
    monkeypatch.setattr(Screen, "isPlain", lambda: False)
    for _ in range(3):
        Screen.say("無効なコマンドです。")
    Screen.say("1M進んだ。")
    assert list(Screen.log) == ["無効なコマンドです。 (x3)", "1M進んだ。"]


def test_frame_never_exceeds_a_short_terminal():
    Screen.markSaved(player())
    lines = Screen.frame(["a"], [], "[w]進む [s]戻る [c]メニュー [q]勲章 [save]セーブ [quit]終了", 20, 6)
    assert len(lines) <= 5
    assert lines[-1] == "[quit]終了"


def test_wrap_on_one_column_has_no_empty_or_overflowing_lines():
    assert Screen.wrap("石あ", 1) == ["石", "あ"]


def test_long_list_scrolls_to_keep_the_cursor_visible():
    stones = Screen.table([["石%d" % i, "1.0CM"] for i in range(30)], 25)
    lines = Screen.frame(stones, [], "[x]戻る", 40, 12)
    assert any(line.startswith("> 石25") for line in lines)


def test_plain_confirmation_shows_again_after_returning_to_a_list(monkeypatch, capsys):
    keys_from(monkeypatch, "x", "x", "x", "x", "x")
    for _ in range(2):
        Screen.scene("石カバンを投げつけて逃走することができます。")
        Screen.ask("[z]よろしい [x]やめる")
        Screen.rows(["> 赤弾 x50"])
        Screen.ask("[x]諦める")
    assert capsys.readouterr().out.count("石カバンを投げつけて") == 2


def test_page_footer_offers_page_numbers(db, monkeypatch, capsys):
    from CollectionBook import CollectionBook
    keys_from(monkeypatch, "1", "x", "x")
    data = DB.load("wada")
    data.m = -1
    CollectionBook().openBook(data)
    assert capsys.readouterr().out.count("[番号]ページを見る") == 2
