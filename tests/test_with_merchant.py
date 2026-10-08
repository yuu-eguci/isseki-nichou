from types import SimpleNamespace

from WithMerchant import WithMerchant


def test_check_stone_with_empty_bag_does_not_crash():
    data = SimpleNamespace(attr="browseStones", stonesList=[], cursor=0)
    data = WithMerchant().checkStone(data)
    assert data.attr == "browseStones"


def test_selling_last_stone_keeps_cursor_in_bag():
    data = SimpleNamespace(
        attr="checkStone", stonesList=["ラポ@2.0CM", "テンラグ@1.0CM"],
        cursor=1, price=100, gold=0,
    )
    data = WithMerchant().sellStone(data)
    assert data.stonesList == ["ラポ@2.0CM"]
    assert data.gold == 100
    assert data.cursor == 0
