from Data import Data


def make_dic(**overrides):
    dic = {
        "id": 1, "name": "yuu", "field": "Nagoya", "m": 3,
        "stones": "クズ石@1.0CM,石@(未鑑定)@ラポ@2.0CM",
        "guns": "汎用駆除銃@1", "bullets": "赤弾@50,青弾@50,黒弾@50",
        "gold": 1000, "score": "", "trophy": "クリアー|||Python,Robber",
    }
    dic.update(overrides)
    return dic


def test_csv_columns_become_lists():
    data = Data(make_dic())
    assert data.stonesList == ["クズ石@1.0CM", "石@(未鑑定)@ラポ@2.0CM"]
    assert data.bulletsList == ["赤弾@50", "青弾@50", "黒弾@50"]
    assert data.trophiesList == ["クリアー"]
    assert data.troDataList == ["Python", "Robber"]


def test_empty_columns_become_empty_lists():
    data = Data(make_dic(stones="", score="", trophy="|||"))
    assert data.stonesList == []
    assert data.scoreList == []
    assert data.trophiesList == []
    assert data.troDataList == []


def test_camp_position_restarts_at_zero():
    assert Data(make_dic(m=-1)).m == 0
