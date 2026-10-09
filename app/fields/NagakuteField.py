# !/usr/bin/env python
# coding: utf-8

# NagakuteField

from CommonFunctions import *
import Screen
from NagakuteEvents  import *
from Inventory       import *
from Trophy          import *

class NagakuteField(NagakuteEvents):
    def __init__(self, data):
        self.data = data

    def fieldMain(self, data):
        while 1:
            # 現在何メートルにいるかはヘッダーに表示されます。
            Screen.scene("今にも降り出しそうな曇天が影を落としている。")

            # キー入力
            key = Screen.ask("[w]進む [s]戻る [c]メニュー [q]勲章 [save]セーブ", quit=True)
            data = self.inputKey(key, data, ["w","s","c","save","q"])

            # self.mの値によってはJunctionに戻ったり固定イベントが発生する
            if data.m == -1:
                return data

            # self.fieldの値によってはfieldJunctionへ戻る
            if data.field != "Nagakute":
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


