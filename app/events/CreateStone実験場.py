# !/usr/bin/env python
# coding: utf-8

# ==============================
# CreateStoneのpop度設定で実際どれくらい出るのか測定する
# field名を書くところがあるからそこを書けば動きます
# ==============================
# フィールドはどこ?
field = "Nagakute"

import random
from CreateStone import *

def createStone(field):
    stoneList = []
    for stone in CreateStone.stones:
        if stone in eval("CreateStone." + field + "Stones"):
            stoneList.append(stone)
    popList   = [CreateStone.stones[stone]["pop"] for stone in stoneList]

    maximum = sum(popList)
    target = random.randint(1, maximum)
    i = 0
    for index in range(len(popList)):
        i += popList[index]
        if target <= i:
            return list(stoneList)[index]

def countPop(field):
    # ==============================
    # popの合計を求める
    # ==============================
    stoneList = []
    for stone in CreateStone.stones:
        if stone in eval("CreateStone." + field + "Stones"):
            stoneList.append(stone)
    popList   = [CreateStone.stones[stone]["pop"] for stone in stoneList]
    return sum(popList)



# 結果確認用ディクショナリ作成
resultDic = {}
for stone in eval("CreateStone." + field + "Stones"):
    resultDic[stone] = 0
# {'ruby': 0, 'lapislazuli': 0, 'garnet': 0, 'aquamarine': 0,...}

# 実際に pop合計 * 100 回まわす
times = 100 * countPop(field)
for i in range(times):
    resultDic[createStone(field)] += 1

# 結果をリスト順に並べる
for stone in eval("CreateStone." + field + "Stones"):
    per = round(resultDic[stone] / times * 100)
    print("%s:%s-%s%%," % (stone, resultDic[stone], per), end=" ")

