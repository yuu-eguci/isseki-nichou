# !/usr/bin/env python
# coding: utf-8

# ==============================
# キー入力による分岐を作るクラス
# ==============================

from CommonFunctions import *
from DB              import *

class InputKey:
    # ==============================
    # 分岐 acceptListに指定されたキーしか選択できない
    # ==============================
    def inputKey(self, key, data, acceptList):
        if key in acceptList or key.lower() in acceptList:
            data = eval("self.input" + key.upper())(data)
            return data
        else:
            systemDis0("無効なコマンドです。")
            return data

    # ==============================
    # 具体的な処理は個々のサブクラスに書く
    # ==============================
    def inputW(self, data):
        return data
    def inputS(self, data):
        return data
    def inputA(self, data):
        return data
    def inputD(self, data):
        return data
    def inputZ(self, data):
        return data
    def inputX(self, data):
        return data
    def inputC(self, data):
        return data
    def inputSAVE(self, data):
        DB.save(data)
        return data
    def inputQ(self, data):
        return data

if __name__ == "__main__":
    key = "c"
    instance = InputKey()
    instance.inputKey(key)
