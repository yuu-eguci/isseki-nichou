# !/usr/bin/env python
# coding: utf-8

# 勲章の管理

from CommonFunctions import *
from InputKey        import *
import Screen

class Trophy(InputKey):
    trophiesList = [
        {"クリアー":"石をすべて収集し、自由の身になりました。"},
        {"極めクリアー":"すべての石の5.0CMを収集し、自由の身になりました。"},
        {"ボス殲滅完了":"すべてのボス害獣を駆除しました。"},
        ]

    # ==============================
    # 勲章とスコアを表示する
    # ==============================
    def browseTrophies(self, data):
        data.attr = "browseTrophies"
        # カーソル位置の初期化
        data.cursor = 0
        while 1:
            # 勲章のリストを作る data.trophiesList の文字列と一致してるものだけ表示する
            cells = []
            for i, trophy in enumerate(Trophy.trophiesList):
                name = list(trophy.keys())[0]
                tmp2 = (": %s" % list(trophy.values())[0]) if data.cursor == i else ""
                cells.append([name if name in data.trophiesList else "????", tmp2])
            Screen.scene("勲章")
            Screen.rows(Screen.table(cells, data.cursor))

            # スコアの履歴を表示する
            if data.scoreList:
                Screen.rows(["", "クリアスコアの履歴です。"])
                Screen.rows(Screen.table([score.split("|") for score in data.scoreList]))

            # キー入力
            key = Screen.ask("[w/s]勲章と説明を見る [x]戻る")
            data = self.inputKey(key, data, ["w","s","x"])

            if data.attr != "browseTrophies":
                return data

    # ==============================
    # キーイベント
    # ==============================
    def inputW(self, data):
        if data.cursor != 0:
            data.cursor -= 1
        return data

    def inputS(self, data):
        if data.cursor != (len(Trophy.trophiesList) - 1):
            data.cursor += 1
        return data

    def inputX(self, data):
        data.attr = ""
        return data
