# !/usr/bin/env python
# coding: utf-8

# 勲章の管理

from CommonFunctions import *
from InputKey        import *

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
            systemDis0("上下(w,s)で勲章と説明を見る 'x'で戻ります。")

            # 勲章のリストを作る data.trophiesList の文字列と一致してるものだけ表示する
            i = 0
            for trophy in Trophy.trophiesList:
                tmp1 = "==>" if data.cursor == i else ""
                tmp2 = (": %s" % list(Trophy.trophiesList[i].values())[0]) if data.cursor == i else ""
                if not list(trophy.keys())[0] in data.trophiesList:
                    trophy = "????"
                    invDis("%s %s %s" % (tmp1, trophy, tmp2))
                else:
                    invDis("%s %s %s" % (tmp1, list(trophy.keys())[0], tmp2))
                i += 1

            # スコアの履歴を表示する
            if data.scoreList:
                systemDis0("クリアスコアの履歴です。")
                for score in data.scoreList:
                    scoreANDdate = score.split("|")
                    invDis("%s (%s)" % (scoreANDdate[0], scoreANDdate[1]))
            print("\n")

            # キー入力
            key = input()
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
