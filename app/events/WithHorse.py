# !/usr/bin/env python
# coding: utf-8

# WithHorse

from CommonFunctions import *
from InputKey        import *

class WithHorse(InputKey):
    def talkHorse(self, data):
        data.attr = "talkHorse"
        while 1:
            if data.attr != "talkHorse":
                return data
            systemDis0("武装馬車の御者がこちらを見ている。「500金になるよ」")
            systemDis("'z'で支払う 'x'でやめます。")
            # キー入力
            key  = input()
            data = self.inputKey(key, data, ["z","x"])

    def payFare(self, data):
        if data.gold < 500:
            systemDis0("手持ちが足りない。「スマンが慈善事業じゃないのじゃ」")
        else:
            data.gold -= 500
            data.m     = 0
            data.attr  = ""
            systemDis0("500金支払ってキャンプの前まで移動しました。「まいど」")
        return data

    # ==============================
    # キーイベント
    # ==============================
    def inputZ(self, data):
        data = self.payFare(data)
        return data
    def inputX(self, data):
        data.attr = ""
        return data
