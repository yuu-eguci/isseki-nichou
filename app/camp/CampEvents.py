# !/usr/bin/env python
# coding: utf-8

# CampEvent

from CommonFunctions import *
from InputKey        import *
from Inventory       import *

class CampEvents(InputKey):
    # ==============================
    # 石の鑑定 stonesListの要素から"石@(未鑑定)@"をはぶく self.mが-2ならここへ来る
    # ==============================
    def judgeStones(self, data):
        for i in range(len(data.stonesList)):
            data.stonesList[i] = data.stonesList[i].replace("石@(未鑑定)@", "")
        systemDis0("手持ちの石(未鑑定)を鑑定しました。「もとには戻せないからね」")
        return data

    # ==============================
    # 弾の補充 個数が0の弾をいっこずつ補充する
    # ==============================
    def stockBullets(self, data):
        flag = False
        systemDis0("残弾数ゼロの弾のみ補充できます。")
        for i in range(len(data.bulletsList)):
            nameANDnum = data.bulletsList[i].split("@")
            if int(nameANDnum[1]) <= 0:
                # 自己レビューにより、補給はもっとあっていいだろと出た。増やす。1->20
                data.bulletsList[i] = nameANDnum[0] + "@10"
                systemDis0("%s を補充しました。" % nameANDnum[0])
                flag = True
        if not flag:
            systemDis0("残弾数ゼロの弾がありません。")
        return data

    # ==============================
    # キーイベント
    # ==============================
    def inputX(self, data):
        data.m = -1
        return data
    def inputC(self, data):
        inventory = Inventory()
        data = inventory.menu(data)
        del inventory
        data.m = -1
        return data

