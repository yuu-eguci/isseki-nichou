# !/usr/bin/env python
# coding: utf-8

import random

class CreateStone:
    # 全部の石の情報 popは出やすさ。数値の小さいほうがレア
    stones = {
        "dust"        : {"pop":5, "name" :"クズ石",
                                  "name2":"クズ石"},

        "diamond"     : {"pop":1, "page":1, "column":1, "name" :"ドノマイド",
                         "price":500,                   "name2":"ダイアモンド"},
        "ruby"        : {"pop":2, "page":1, "column":2, "name" :"イブル",
                         "price":300,                   "name2":"ルビー"},
        "sapphire"    : {"pop":2, "page":1, "column":3, "name" :"エリファス",
                         "price":300,                   "name2":"サファイア"},
        "emerald"     : {"pop":3, "page":1, "column":4, "name" :"ドラレメ",
                         "price":100,                   "name2":"エメラルド"},
        "lapislazuli" : {"pop":3, "page":1, "column":5, "name" :"イルザルシパル",
                         "price":100,                   "name2":"ラピスラズリ"},
        "opal"        : {"pop":3, "page":1, "column":6, "name" :"ラポ",
                         "price":100,                   "name2":"オパール"},
        "turquoise"   : {"pop":3, "page":1, "column":7, "name" :"エショウクルット",
                         "price":100,                   "name2":"ターコイズ"},
        "garnet"      : {"pop":3, "page":1, "column":8, "name" :"テンラグ",
                         "price":100,                   "name2":"ガーネット"},
        "aquamarine"  : {"pop":3, "page":1, "column":9, "name" :"エニラマウカ",
                         "price":100,                   "name2":"アクアマリン"},
        "topaz"       : {"pop":3, "page":1, "column":10, "name" :"ザポット",
                         "price":100,                    "name2":"トパーズ"},

        "alexandrite" : {"pop":1, "page":2, "column":1, "name" :"エティルドナグゼラ",
                         "price":500,                   "name2":"アレキサンドライト"},
        "amethyst"    : {"pop":2, "page":2, "column":2, "name" :"トシセマ",
                         "price":300,                   "name2":"アメシスト"},
        "citrine"     : {"pop":2, "page":2, "column":3, "name" :"エニルチック",
                         "price":300,                   "name2":"シトリン"},
        "peridot"     : {"pop":3, "page":2, "column":4, "name" :"オディレプ",
                         "price":100,                   "name2":"ペリドット"},
        "tanzanite"   : {"pop":3, "page":2, "column":5, "name" :"エティナズナット",
                         "price":100,                   "name2":"タンザナイト"},
        "malachite"   : {"pop":3, "page":2, "column":6, "name" :"エティカラム",
                         "price":100,                   "name2":"マラカイト"},
        "chrysocolla" : {"pop":3, "page":2, "column":7, "name" :"アロコシルク",
                         "price":100,                   "name2":"クリソコラ"},
        "jade"        : {"pop":3, "page":2, "column":8, "name" :"エダージュ",
                         "price":100,                   "name2":"ジェイド"},
        "agate"       : {"pop":3, "page":2, "column":9, "name" :"エターガ",
                         "price":100,                   "name2":"アガーテ"},
        "iolite"      : {"pop":3, "page":2, "column":10, "name" :"エティロイ",
                         "price":100,                    "name2":"アイオライト"},
        }

    # エリアごとの出現石一覧
    NagoyaStones = [
        # "dust"       ,
        "diamond"    ,
        "ruby"       ,
        "sapphire"   ,
        "emerald"    ,
        "lapislazuli",
        "opal"       ,
        "turquoise"  ,
        "garnet"     ,
        "aquamarine" ,
        "topaz"      ,
        ]
    NagakuteStones = [
        # "dust"       ,
        "alexandrite",
        "amethyst"   ,
        "citrine"    ,
        "peridot"    ,
        "tanzanite"  ,
        "malachite"  ,
        "chrysocolla",
        "jade"       ,
        "agate"      ,
        "iolite"     ,
        ]

    # 大きさ(整数部分)のレア度とリストづくり
    sizes = {
        "5" : {"pop":1},
        "4" : {"pop":2},
        "3" : {"pop":3},
        "2" : {"pop":4},
        "1" : {"pop":5},
        "0" : {"pop":6},
        }
    sizeLis = []
    for size in sizes:
        sizeLis += size * sizes[size]["pop"]

    # ==============================
    # field名を受け取り、そのフィールドでpopする石の中からランダムで造って返す
    # べつにインスタンスメソッドである必要はないからクラスメソッドだよ。
    # ==============================
    def createStone(field):
        # stoneList(候補の石名) popList(stoneListのpopリスト) を作る
        stoneList = []
        for stone in CreateStone.stones:
            if stone in eval("CreateStone." + field + "Stones"):
                stoneList.append(stone)
        popList = [CreateStone.stones[stone]["pop"] for stone in stoneList]
        # stoneList: ['topaz', 'lapislazuli', 'diamond',...]
        # popList  : [3, 3, 1, 3, 5,...] って感じになるよ

        maximum = sum(popList)
        target = random.randint(1, maximum)
        i = 0
        for index in range(len(popList)):
            i += popList[index]
            if target <= i:
                result1 = CreateStone.stones[list(stoneList)[index]]["name"]
                break

        # 大きさを選ぶ
        result2 = random.choice(CreateStone.sizeLis)
        if   result2 == "5":
            result2 += ".0CM"
        else:
            result2 += "." + str(random.randint(0, 9)) + "CM"

        # 0.0CMってことがありえた
        if result2 == "0.0CM":
            result2 = "0.1CM"

        result = result1 + "@" + result2
        return result

if __name__ == "__main__":
    fieldName = "Nagoya"
    print(CreateStone.createStone(fieldName))
