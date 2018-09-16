# !/usr/bin/env python
# coding: utf-8

# NagoyaField

from CommonFunctions import *
from NagoyaEvents    import *
from Inventory       import *
from Trophy          import *

class NagoyaField(NagoyaEvents):
    def __init__(self, data):
        self.data = data

    def fieldMain(self, data):
        while 1:
            # 現在何メートルにいるか表示する
            systemDis0("草木が微風にそよいでいる。")
            systemDis0("現在ナゴヤ・エリア %d M 地点です。" % data.m)
            systemDis("'w'で進む 's'で戻る 'c'でメニュー 'save'でセーブできます。")

            # キー入力
            key = input()
            data = self.inputKey(key, data, ["w","s","c","save","q"])

            # self.mの値によってはJunctionに戻ったり固定イベントが発生する
            if data.m == -1:
                return data

            # self.fieldの値によってはfieldJunctionへ戻る
            if data.field != "Nagoya":
                return data

    # ==============================
    # キーイベント
    # ==============================
    def inputW(self, data):
        systemDis0("1M進んだ。")
        data.m += 1
        if data.m != -1:
            data = self.eventJunction(data)
        return data
    def inputS(self, data):
        systemDis0("1M戻った。")
        data.m -= 1
        if data.m != -1:
            data = self.eventJunction(data)
        return data
    def inputC(self, data):
        inventory = Inventory()
        data = inventory.menu(data)
        del inventory
        return data
    def inputQ(self, data):
        tro = Trophy()
        data = tro.browseTrophies(data)
        del tro
        return data


