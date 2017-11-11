# !/usr/bin/env python
# coding: utf-8

from CommonFunctions import *
from DB              import *
from FieldJunction   import *

class Start:
    def start(self):
        ### 名前を入力してセーブを読み込む ###
        while 1:
            systemDis0("こんにちは。ロードするデータの名前を入力してください。")
            systemDis("新しくデータを作る場合は'make 'のあとに作るデータの名前を入力してください。")

            key = input()

            if key.startswith("make "):
                # 新規登録する
                newName = key.replace("make ", "")
                if   newName.startswith("make "):
                    systemDis("データ名は'make 'からは始められません。別の名前を入力してください。")
                elif newName.count("@"):
                    systemDis("データ名に'@'は使えません。別の名前を入力してください。")
                else:
                    if DB.makeData(newName):
                        # 新規登録して、そのデータをロードして開始する
                        data = DB.load(newName)
                        if data:
                            FieldJunction.fieldJunction(data)
                    else:
                        systemDis("既存のデータ名と重複しています。別の名前を入力してください。")
            else:
                # 既存のデータをロードして開始する
                data = DB.load(key)
                if data:
                    FieldJunction.fieldJunction(data)

if __name__ == "app.Start":
    kill = Start()
    kill.start()
