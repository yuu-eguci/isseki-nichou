from types import SimpleNamespace

from GunFunctions import addDamage, addMessageN, addMessageW


def test_normal_gun_adds_nothing():
    data = SimpleNamespace(gunsList=["汎用駆除銃@1"])
    assert addDamage(data) == 0
    assert addMessageW(data) == "この弾はよく効いているようだ。2ダメージを与えた。"


def test_clear_reward_gun_adds_mark_plus_one():
    data = SimpleNamespace(gunsList=["猟銃yuuマーク2@1", "汎用駆除銃@1"])
    assert addDamage(data) == 3
    assert addMessageN(data).endswith("4ダメージを与えた。")


def test_tenth_clear_reward_gun_uses_whole_mark_number():
    data = SimpleNamespace(gunsList=["猟銃yuuマーク10@1"])
    assert addDamage(data) == 11
