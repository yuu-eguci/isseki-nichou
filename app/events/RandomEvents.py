# !/usr/bin/env python
# coding: utf-8

# RandomEvents

from CommonFunctions import *
from InputKey        import *
from CreateStone     import *
from KickEnemy       import *
import random

class RandomEvents(InputKey):
    # 出現するランダム敵
    NagoyaEnemies   = ["Alligator", "Hornet"]
    NagakuteEnemies = ["Tarantula", "Leopard"]

    def randomEvent(self, data):
        rand = random.randint(1, 10)
        if   rand <= 1:
            # 出現する敵を選択
            data.enemy = random.choice(eval("RandomEvents." + data.field + "Enemies"))
            self.encounterEnemy(data)
        elif rand >= 10:
            self.findStone(data)
        return data

    # ==============================
    # がおー
    # ==============================
    def encounterEnemy(self, data):
        data.attr = "enemy"
        while 1:
            systemDis0("ランダムイベント: そのへんの草むらが気になる…。")
            systemDis("'z'で調べる 'x'でそそくさと離れる。")

            # キー入力
            key = input()
            data = self.inputKey(key, data, ["z","x"])

            if data.attr != "enemy":
                return data

    # ==============================
    # 石を拾う
    # ==============================
    def findStone(self, data):
        data.attr = "stone"
        while 1:
            systemDis0("ランダムイベント: そのへんの草むらが気になる…。")
            systemDis("'z'で調べる 'x'でそそくさと離れる。")

            # キー入力
            key = input()
            data = self.inputKey(key, data, ["z","x"])

            # xが押されたらreturn
            if data.attr != "stone":
                return data

    def foundStone(self, data):
        # 石を内部的に追加する
        data.stonesList.append("石@(未鑑定)@" + CreateStone.createStone(data.field))
        while 1:
            systemDis0("気になる石を見つけた。「価値のあるものかもしれない」")
            systemDis0("持ち物に石(未鑑定)を追加しました。")
            systemDis("'x'でこの場を離れる。")

            # キー入力
            key = input()
            data = self.inputKey(key, data, ["x"])

            # xが押されたらreturn
            if data.attr == "":
                return data

    # ==============================
    # キーイベント
    # ==============================
    def inputZ(self, data):
        if   data.attr == "enemy":
            # encounterEnemyから呼ばれたときは駆除開始
            battle = KickEnemy()
            data = battle.kickEnemy(data)
            del battle
        elif data.attr == "stone":
            # findStoneから呼ばれたとき
            self.foundStone(data)
        return data
    def inputX(self, data):
        systemDis0("その場を離れた。")
        data.attr = ""
        return data

