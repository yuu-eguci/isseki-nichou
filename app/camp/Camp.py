# !/usr/bin/env python
# coding: utf-8

# Camp
# mが-1だとJunctionからここへ来る

from CommonFunctions import *
import Screen
from InputKey        import *
from CampEvents      import *
from CollectionBook  import *

class Camp(CampEvents):
    def __init__(self, data):
        self.data = data

    def fieldMain(self, data):
        roop = 0
        while 1:
            # self.mの値によってはfieldJunctionへ戻る。
            if self.data.m != -1:
                return self.data

            # ループ一周目だけおかえりメッセージを出す。
            if roop == 0:
                systemDis0("キャンプに這入りました。「無事でなにより」")
                roop += 1
            else:
                Screen.scene("現在キャンプにいます。")

            # キー入力
            key = Screen.ask("[w]キャンプを出る [a]石(未鑑定)の鑑定 [s]弾の補充 [d]収集本を見る", quit=True)
            self.data = self.inputKey(key, self.data, ["w","s","a","d"])

    # ==============================
    # キーイベント
    # ==============================
    def inputW(self, data):
        systemDis0("キャンプを出ました。")
        data.m += 1
        return data
    def inputS(self, data):
        data = self.stockBullets(data)
        return data
    def inputA(self, data):
        data = self.judgeStones(data)
        return data
    def inputD(self, data):
        book = CollectionBook()
        data = book.openBook(data)
        return data



