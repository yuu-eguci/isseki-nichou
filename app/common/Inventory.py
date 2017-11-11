# !/usr/bin/env python
# coding: utf-8

# Inventory つまりはフィールドで開くことのできるメニュー画面
# つかうときはインスタントインスタンスにしてくれたまえ

from CommonFunctions import *
from InputKey        import *

class Inventory(InputKey):
    # ==============================
    # メニュー選択
    # ==============================
    def menu(self, data):
        data.attr = "menu"
        while 1:
            systemDis0("現在の所持金は %s です。" % data.gold)
            systemDis("'a'で石カバンを見る 'd'で武器を見る 'x'で戻ります。")

            # キー入力
            key = input()
            data = self.inputKey(key, data, ["a","d","x"])

            if data.attr == "":
                del data.attr
                return data

    # ==============================
    # 石カバンを見る
    # ==============================
    def browseStones(self, data):
        data.attr = "browseStones"
        # カーソル位置の初期化
        data.cursor = 0
        while 1:
            systemDis0("上下('w','s')で石を選ぶ 'a'で石を整理する")
            systemDis0("'d'で選んだ石を捨てる 'c'ですべて捨てる 'x'で戻ります。")

            # 石のリストを作る
            i = 0
            for stone in data.stonesList:
                nameANDcm = stone.split("@")
                tmp = "==>" if data.cursor == i else ""
                invDis("%s %s %s" % (tmp, nameANDcm[0], nameANDcm[1]))
                i += 1
            print("\n")

            # キー入力
            key = input()
            data = self.inputKey(key, data, ["w","s","a","d","c","x"])

            if data.attr != "browseStones":
                return data

    # ==============================
    # 石を捨てる
    # ==============================
    def throwStone(self, data):
        data.attr = "throwStone"

        # 石がひとつもないときにここへ来たらreturn
        if len(data.stonesList) == 0:
            systemDis0("石がひとつもありません。")
            data.attr = "browseStones"
            return data

        while 1:
            nameANDcm   = data.stonesList[data.cursor].split("@")
            # inputZの中でいちいちtargetを作り直したくないのでdataに刻んで渡す
            data.target = "%s %s" % (nameANDcm[0], nameANDcm[1])
            systemDis0("%s を捨てますがよろしいですか。" % data.target)
            systemDis("'z'で捨てる 'x'でキャンセル。")

            # キー入力
            key = input()
            data = self.inputKey(key, data, ["z","x"])

            if data.attr != "throwStone":
                return data

    # ==============================
    # ぜんぶ捨てる
    # ==============================
    def dumpStones(self, data):
        data.attr = "dumpStones"

        # 石がひとつもないときにここへ来たらreturn
        if len(data.stonesList) == 0:
            systemDis0("石がひとつもありません。")
            data.attr = "browseStones"
            return data

        while 1:
            systemDis0("カバンの中の石をすべて捨てますがよろしいですか。")
            systemDis("'z'で捨てる 'x'でキャンセル。")

            # キー入力
            key = input()
            data = self.inputKey(key, data, ["z","x"])

            if data.attr != "dumpStones":
                return data

    # ==============================
    # 石カバンのソート data.stonesListをpatternListの順に並べ替える
    # ==============================
    def sortStones(self, data):
        # ソートの順番
        patternList = [
            "ドノマイド",
            "イブル",
            "エリファス",
            "ドラレメ",
            "イルザルシパル",
            "ラポ",
            "エショウクルット",
            "テンラグ",
            "エニラマウカ",
            "ザポット",
            "エティルドナグゼラ",
            "トシセマ",
            "エニルチック",
            "オディレプ",
            "エティナズナット",
            "エティカラム",
            "アロコシルク",
            "エダージュ",
            "エターガ",
            "エティロイ",
            "クズ石",
            "未鑑定",
            ]
        patternDict = {
            "ドノマイド":[],
            "イブル":[],
            "エリファス":[],
            "ドラレメ":[],
            "イルザルシパル":[],
            "ラポ":[],
            "エショウクルット":[],
            "テンラグ":[],
            "エニラマウカ":[],
            "ザポット":[],
            "エティルドナグゼラ":[],
            "トシセマ":[],
            "エニルチック":[],
            "オディレプ":[],
            "エティナズナット":[],
            "エティカラム":[],
            "アロコシルク":[],
            "エダージュ":[],
            "エターガ":[],
            "エティロイ":[],
            "クズ石":[],
            "未鑑定":[],
            }
        # patternDictのリストに手持ちの石のcmを追加していく
        for stone in data.stonesList:
            nameANDcm = stone.split("@")

            # 未鑑定品はまるごとよけとく
            if nameANDcm[1] == "(未鑑定)":
                patternDict["未鑑定"].append(stone)
            else:
                cm = float(nameANDcm[1].replace("CM", ""))
                patternDict[nameANDcm[0]].append(cm)

        # patternDictの中身をpatternList順にリスト化する
        newList = []
        for name in patternList:
            lis = patternDict[name]
            lis.sort()
            lis.reverse()
            if lis and name != "未鑑定":
                for cm in lis:
                    stone = name + "@" + str(cm) + "CM"
                    newList.append(stone)
            elif lis and name == "未鑑定":
                for thing in lis:
                    newList.append(thing)

        # でそれをdata.stonesListとする
        data.stonesList = newList
        systemDis0("石カバンの中身を整理しました。")
        return data

    # ==============================
    # 武器を見る
    # ==============================
    def browseWeapons(self, data):
        data.attr = "browseWeapons"
        # カーソル位置の初期化
        data.cursor = 0
        while 1:
            systemDis0("上下('w','s')で武器を選ぶ 'z'で選んだ銃を装備する 'x'で戻ります。")

            # 武器のリストを作る
            i = 0
            for gun in data.gunsList:
                nameANDcm = gun.split("@")
                tmp = "==>" if data.cursor == i else ""
                equ = "装備中" if i == 0 else ""
                invDis("%s %s *%s %s" % (tmp, nameANDcm[0], nameANDcm[1], equ))
                i += 1
            for bullet in data.bulletsList:
                nameANDcm = bullet.split("@")
                tmp = "==>" if data.cursor == i else ""
                invDis("%s %s *%s" % (tmp, nameANDcm[0], nameANDcm[1]))
                i += 1
            print("\n")

            # キー入力
            key = input()
            data = self.inputKey(key, data, ["w","s","z","x"])

            if data.attr != "browseWeapons":
                return data

    # ==============================
    # 武器を替える
    # ==============================
    def changeGun(self, data):
        if data.cursor >= len(data.gunsList):
            # 選択中なのが弾だったら何もやらない
            systemDis0("弾を装備する必要はありません。")
        elif data.cursor == 0:
            # 装備中の銃を選択してる
            systemDis0("その銃はすでに装備中です。")
        else:
            # 選択中の銃をgunsListの先頭に移動させる
            tmp = data.gunsList[data.cursor]
            data.gunsList.pop(data.cursor)
            data.gunsList.insert(0, tmp)
            systemDis0("%s を装備しました。" % data.gunsList[0])
        return data

    # ==============================
    # キーイベント
    # ==============================
    def inputA(self, data):
        if   data.attr == "menu":
            data = self.browseStones(data)
        elif data.attr == "browseStones":
            data = self.sortStones(data)
        return data

    def inputD(self, data):
        if   data.attr == "menu":
            data = self.browseWeapons(data)
        elif data.attr == "browseStones":
            data = self.throwStone(data)
        return data

    def inputC(self, data):
        if   data.attr == "browseStones":
            data = self.dumpStones(data)
        return data

    def inputZ(self, data):
        if   data.attr == "throwStone":
            systemDis0("%s を捨てました。「それ、飛んで行け!」ﾎﾟｰｲ" % data.target)
            data.stonesList.pop(data.cursor)
            del data.target
            data = self.browseStones(data)
        elif data.attr == "dumpStones":
            systemDis0("石をすべて捨てました。「それ、さようなら!」ﾊﾞﾗﾊﾞﾗ")
            data.stonesList = []
            data = self.browseStones(data)
        elif data.attr == "browseWeapons":
            data = self.changeGun(data)
        return data

    def inputX(self, data):
        if   data.attr == "menu":
            data.attr = ""
        elif data.attr == "browseStones":
            data.attr = ""
        elif data.attr == "throwStone":
            data = self.browseStones(data)
        elif data.attr == "dumpStones":
            data = self.browseStones(data)
        elif data.attr == "browseWeapons":
            data.attr = ""
        return data

    def inputW(self, data):
        if   data.attr == "browseStones" and data.cursor != 0:
            data.cursor -= 1
        elif data.attr == "browseWeapons" and data.cursor != 0:
            data.cursor -= 1
        return data

    def inputS(self, data):
        if   data.attr == "browseStones" and data.cursor != (len(data.stonesList) - 1):
            data.cursor += 1
        elif data.attr == "browseWeapons" and data.cursor != (len(data.gunsList) + len(data.bulletsList) - 1):
            data.cursor += 1
        return data
