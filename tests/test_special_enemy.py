from types import SimpleNamespace

from SpecialEnemy import SpecialEnemy


def test_robber_prize_is_a_whole_stone_name():
    data = SimpleNamespace(
        bulletsList=["赤弾@5"], cursor=0, gunsList=["汎用駆除銃@1"],
        enHp=1, myHp=3, anti=["青"], his=["weak"],
        stonesList=[], gold=5000, troDataList=[],
    )
    data = SpecialEnemy.shootRobber(data)
    name, size = data.stonesList[0].split("@")
    assert name in SpecialEnemy.scorpionsList
    assert size == "5.0CM"
    assert data.gold == 7000
