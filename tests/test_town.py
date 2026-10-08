"""商人、馬車、キャンプ、持ち物の現在の挙動を固定するテストです。"""
from types import SimpleNamespace

from CampEvents import CampEvents
from InputKey import InputKey
from Inventory import Inventory
from WithHorse import WithHorse
from WithMerchant import WithMerchant


def test_merchant_buys_stone_for_price_times_size(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda: "z")
    data = SimpleNamespace(attr="browseStones", stonesList=["クズ石@1.0CM", "ラポ@2.5CM"], cursor=1, gold=0)
    data = WithMerchant().checkStone(data)
    assert data.gold == 250
    assert data.stonesList == ["クズ石@1.0CM"]


def test_merchant_bulk_sale_keeps_dust_and_unappraised(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda: "z")
    stones = ["クズ石@1.0CM", "石@(未鑑定)@ラポ@2.0CM", "ドノマイド@1.0CM", "イブル@2.0CM"]
    data = SimpleNamespace(attr="browseStones", stonesList=stones, cursor=0, gold=0)
    data = WithMerchant().checkAllStones(data)
    assert data.gold == 1100
    assert data.stonesList == ["クズ石@1.0CM", "石@(未鑑定)@ラポ@2.0CM"]


def test_merchant_sells_bullet_only_when_affordable():
    data = SimpleNamespace(attr="checkBullet", cursor=0, gold=99, bulletsList=["赤弾@1", "青弾@1", "黒弾@1"])
    data = WithMerchant().buyBullet(data)
    assert (data.gold, data.bulletsList[0]) == (99, "赤弾@1")
    data.gold = 150
    data = WithMerchant().buyBullet(data)
    assert (data.gold, data.bulletsList[0]) == (50, "赤弾@2")


def test_horse_fare_takes_you_to_camp_front():
    data = WithHorse().payFare(SimpleNamespace(gold=499, m=45, attr="talkHorse"))
    assert (data.gold, data.m) == (499, 45)
    data = WithHorse().payFare(SimpleNamespace(gold=500, m=45, attr="talkHorse"))
    assert (data.gold, data.m, data.attr) == (0, 0, "")


def test_camp_refills_only_empty_bullets():
    data = SimpleNamespace(bulletsList=["赤弾@0", "青弾@3", "黒弾@0"])
    data = CampEvents().stockBullets(data)
    assert data.bulletsList == ["赤弾@10", "青弾@3", "黒弾@10"]


def test_camp_appraises_stones():
    data = SimpleNamespace(stonesList=["石@(未鑑定)@ラポ@2.0CM", "クズ石@1.0CM"])
    data = CampEvents().judgeStones(data)
    assert data.stonesList == ["ラポ@2.0CM", "クズ石@1.0CM"]


def test_inventory_sorts_by_book_order_then_size():
    stones = ["クズ石@1.0CM", "石@(未鑑定)@ラポ@2.0CM", "ラポ@1.5CM", "ドノマイド@0.5CM", "ラポ@2.5CM"]
    data = Inventory().sortStones(SimpleNamespace(stonesList=stones))
    assert data.stonesList == ["ドノマイド@0.5CM", "ラポ@2.5CM", "ラポ@1.5CM", "クズ石@1.0CM", "石@(未鑑定)@ラポ@2.0CM"]


def test_inventory_equips_selected_gun_first():
    data = SimpleNamespace(gunsList=["汎用駆除銃@1", "猟銃yuuマーク1@1"], cursor=1)
    data = Inventory().changeGun(data)
    assert data.gunsList == ["猟銃yuuマーク1@1", "汎用駆除銃@1"]


def test_input_key_accepts_listed_keys_in_any_case(capsys):
    class Probe(InputKey):
        def inputW(self, data):
            data.pressed = True
            return data

    data = Probe().inputKey("W", SimpleNamespace(pressed=False), ["w"])
    assert data.pressed is True
    data = Probe().inputKey("q", SimpleNamespace(pressed=False), ["w"])
    assert data.pressed is False
    assert "無効なコマンドです。" in capsys.readouterr().out
