"""駆除 (戦闘) の現在の挙動を固定するテストです。"""
from types import SimpleNamespace

import pytest

from CreateStone import CreateStone
from KickEnemy import KickEnemy

BULLETS = ["赤弾@5", "青弾@5", "黒弾@5"]
RED, BLUE, BLACK = 0, 1, 2


def battle(enemy, gun="汎用駆除銃@1", **overrides):
    data = SimpleNamespace(
        enemy=enemy, dic=KickEnemy.enemies[enemy], enHp=KickEnemy.enemies[enemy]["hp"], myHp=3,
        bulletsList=list(BULLETS), gunsList=[gun], cursor=RED, attr="kickEnemy",
        his=[], anti=[], pythonWeak="赤", stonesList=["ラポ@1.0CM"], troDataList=[],
        gold=5000, m=20,
    )
    for key, value in overrides.items():
        setattr(data, key, value)
    return data


def shoot(data, *cursors):
    for cursor in cursors:
        data.cursor = cursor
        data = KickEnemy().shootEnemy(data)
    return data


def nagakute_names():
    return {CreateStone.stones[key]["name"] for key in CreateStone.NagakuteStones}


def test_weak_bullet_does_two_and_normal_bullet_one():
    data = shoot(battle("Alligator"), RED)
    assert (data.enHp, data.myHp) == (1, 2)
    assert data.bulletsList[RED] == "赤弾@4"
    data = shoot(battle("Alligator"), BLUE)
    assert (data.enHp, data.myHp) == (2, 2)


def test_empty_bullet_cannot_be_used():
    data = shoot(battle("Alligator", bulletsList=["赤弾@0", "青弾@5", "黒弾@5"]), RED)
    assert (data.enHp, data.myHp) == (3, 3)


def test_defeating_normal_enemy_ends_battle():
    data = shoot(battle("Alligator"), RED, RED)
    assert data.enHp <= 0
    assert data.attr == ""
    assert data.myHp == 2


def test_losing_drops_stones_and_returns_to_camp():
    data = shoot(battle("Hornet", myHp=2), RED, RED)
    assert data.myHp == 0
    assert (data.stonesList, data.m, data.attr) == ([], -1, "")


def test_giving_up_drops_stones_and_steps_back():
    data = KickEnemy().inputZ(battle("Leopard", attr="giveUp"))
    assert (data.stonesList, data.m, data.attr) == ([], 19, "")


def test_buffalo_rages_after_two_weak_bullets():
    data = shoot(battle("Buffalo"), BLACK, BLACK)
    assert data.myHp == 0
    assert data.m == -1


def test_buffalo_waits_after_two_normal_bullets_and_can_be_beaten():
    data = shoot(battle("Buffalo"), RED, RED)
    assert (data.enHp, data.myHp) == (4, 2)
    data = shoot(data, BLACK, BLACK)
    assert data.attr == ""
    assert data.myHp == 1
    name, size = data.stonesList[-1].split("@")
    assert name in nagakute_names() and size == "5.0CM"
    assert data.troDataList == ["Buffalo"]


def test_python_uses_the_battle_specific_weak_color():
    data = shoot(battle("Python", pythonWeak="青"), BLUE, BLUE, RED)
    assert data.attr == ""
    assert data.troDataList == ["Python"]


def test_scorpions_fall_to_clear_reward_gun_mark_two():
    data = shoot(battle("Scorpions", gun="猟銃yuuマーク2@1"), BLUE, BLUE, BLUE)
    assert data.attr == ""
    assert data.myHp == 1
    assert len(data.stonesList) == 3


def test_scorpions_beat_the_starting_gun():
    data = shoot(battle("Scorpions"), RED, RED, RED)
    assert data.enHp == 4
    assert (data.myHp, data.m) == (0, -1)


def test_robber_antibody_blocks_color_and_weak_hit_skips_counter():
    data = shoot(battle("Robber", anti=["赤"], his=["no"]), RED)
    assert (data.enHp, data.myHp) == (6, 2)
    data = shoot(data, BLUE)
    assert (data.enHp, data.myHp) == (4, 2)
    assert data.anti == ["赤", "青"]
    data = shoot(data, BLACK)
    assert data.anti == ["青", "黒"]


def test_robber_takes_gold_when_you_lose():
    data = shoot(battle("Robber", anti=["赤"], his=["no"], myHp=1), RED)
    assert data.gold == 3000
    assert data.m == -1


@pytest.mark.parametrize("bosses, awarded", [
    (["Python", "Robber", "Scorpions", "Buffalo"], True),
    (["Python", "Robber", "Scorpions"], False),
])
def test_boss_trophy_needs_all_four_bosses(bosses, awarded):
    data = SimpleNamespace(troDataList=bosses, trophiesList=[])
    data = KickEnemy().checkBossTro(data)
    assert ("ボス殲滅完了" in data.trophiesList) is awarded
