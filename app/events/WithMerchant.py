# !/usr/bin/env python
# coding: utf-8

# WithMerchant

from CommonFunctions import *
import Screen
from InputKey        import *
from CreateStone     import *

class WithMerchant(InputKey):
    saleList = ["赤弾@100", "青弾@100", "黒弾@100"]
    explList = ["緑属性の害獣に有効な弾", "黄属性の害獣に有効な弾", "白属性の害獣に有効な弾"]

    def talkMerchant(self, data):
        data.attr = "talkMerchant"
        while 1:
            if data.attr != "talkMerchant":
                return data
            Screen.scene("商人がこちらを見ている。「なにか買う?」")
            # キー入力
            key  = Screen.ask("[a]弾を買う [d]石を売る [x]話をやめる")
            data = self.inputKey(key, data, ["a","d","x"])

    # ==============================
    # 商品リストを見る
    # ==============================
    def browseBullets(self, data):
        data.attr = "browseBullets"
        data.cursor = 0
        while 1:
            if data.attr != "browseBullets":
                return data
            Screen.scene("「100%純正だよ」")

            # 売り物リストを作る
            Screen.rows(Screen.table([[name, gold + "金"] for name, gold in (sale.split("@") for sale in WithMerchant.saleList)], data.cursor))

            # キー入力
            key = Screen.ask("[w/s]選ぶ [z]選んだ弾を買う [x]戻る")
            data = self.inputKey(key, data, ["w","s","z","x"])

    # ==============================
    # 「これを買いますか?」みたいな
    # ==============================
    def checkBullet(self, data):
        data.attr = "checkBullet"
        while 1:
            if data.attr != "checkBullet":
                return data
            Screen.scene("「%sだよ。いいかね」" % (WithMerchant.explList[data.cursor]), "所持金は %s です。" % data.gold)
            price = WithMerchant.saleList[data.cursor].split("@")[1]

            # キー入力
            key = Screen.ask("[z]%s金支払い購入する [x]やめる" % price)
            data = self.inputKey(key, data, ["z","x"])

    # ==============================
    # 購入処理
    # ==============================
    def buyBullet(self, data):
        # saleList[data.cursor]の弾をdata.bulletsListにひとつ追加する
        nameANDgold = WithMerchant.saleList[data.cursor].split("@")
        if data.gold < int(nameANDgold[1]):
            # いやそもそもお金が足りねーってとき
            systemDis0("手持ちが足りない。「石を売ってお金をつくりな」")
        else:
            for i in range(len(data.bulletsList)):
                nameANDnum = data.bulletsList[i].split("@")
                if nameANDgold[0] == nameANDnum[0]:
                    num = int(nameANDnum[1]) + 1
                    data.bulletsList[i] = nameANDnum[0] + "@" + str(num)
            data.gold -= int(nameANDgold[1])
            systemDis0("%s をひとつ買いました。" % nameANDgold[0])
            systemDis0("%s の手持ち %s 個、残りの所持金は %s です。" % (nameANDgold[0], num, data.gold))
        data.attr = "browseBullets"
        return data

    # ==============================
    # 石を見る
    # ==============================
    def browseStones(self, data):
        data.attr = "browseStones"
        data.cursor = 0
        while 1:
            if data.attr != "browseStones":
                return data
            # 石のリストを作る
            Screen.scene("石カバン (%d 個)" % len(data.stonesList))
            Screen.rows(Screen.table([stone.split("@")[:2] for stone in data.stonesList], data.cursor))

            # キー入力
            key = Screen.ask("[w/s]石を選ぶ [z]選んだ石を売る [c]すべて売る [x]戻る")
            data = self.inputKey(key, data, ["w","s","z","c","x"])

    # ==============================
    # 「いくらいくらですがいいかい?」みたいな
    # ==============================
    def checkStone(self, data):
        data.attr = "checkStone"

        # 石がひとつもないときは何もせずに戻ります。
        if len(data.stonesList) == 0:
            systemDis0("石がひとつもありません。")
            data.attr = "browseStones"
            return data

        # 対象の石情報を得る
        target    = data.stonesList[data.cursor]
        nameANDcm = target.split("@")

        # クズ石のとき
        if nameANDcm[0] == "クズ石":
            systemDis0("クズ石は売れない。「それはいらないわ」")
            data.attr = "browseStones"
            return data

        # 未鑑定のとき
        if nameANDcm[1] == "(未鑑定)":
            systemDis0("未鑑定品は売れない。「なんだいこれ?」")
            data.attr = "browseStones"
            return data

        # 売値をはじき出す CreateStone.stonesの"name"をもとに"price"を求めてsizeをかける
        for dic in CreateStone.stones.values():
            if nameANDcm[0] == dic["name"]:
                cm = nameANDcm[1].rstrip("CM")
                data.price = round(dic["price"] * float(cm))

        while 1:
            if data.attr != "checkStone":
                return data
            Screen.scene("%s金で買い取るよ。いいかね" % data.price, "所持金は %s です。" % data.gold)

            # キー入力
            key  = Screen.ask("[z]売却する [x]やめる")
            data = self.inputKey(key, data, ["z","x"])

    # ==============================
    # 「いくらいくらですがいいかい?」みたいな
    # ==============================
    def checkAllStones(self, data):
        data.attr = "checkAllStones"

        # 石の売値をはじき出して全部足す
        data.price = 0
        for stone in data.stonesList:
            nameANDcm = stone.split("@")
            if   nameANDcm[0] == "クズ石":
                pass
            elif nameANDcm[1] == "(未鑑定)":
                pass
            else:
                for dic in CreateStone.stones.values():
                    if nameANDcm[0] == dic["name"]:
                        cm = nameANDcm[1].rstrip("CM")
                        data.price += round(dic["price"] * float(cm))

        while 1:
            if data.attr != "checkAllStones":
                return data
            Screen.scene("%s金で買い取るよ。いいかね" % data.price, "所持金は %s です。" % data.gold)

            # キー入力
            key  = Screen.ask("[z]売却する [x]やめる")
            data = self.inputKey(key, data, ["z","x"])

    # ==============================
    # 売却処理
    # ==============================
    def sellStone(self, data):
        if   data.attr == "checkStone":
            # data.stonesList[data.cursor]の石を削除し、data.priceぶんdata.goldを増やす
            nameANDcm = data.stonesList[data.cursor].split("@")
            data.stonesList.pop(data.cursor)
            data.gold += data.price
            del data.price
            systemDis0("%s %s を売りました" % (nameANDcm[0], nameANDcm[1]))
            systemDis0("現在の所持金は %s です。" % data.gold)
        elif data.attr == "checkAllStones":
            # data.stonesListの、クズ石と未鑑定を除くすべてを削除し、data.priceぶんdata.goldを増やす
            copyList = data.stonesList[:]
            for i in reversed(range(len(data.stonesList))):
                nameANDcm = data.stonesList[i].split("@")
                if   nameANDcm[0] == "クズ石":
                    pass
                elif nameANDcm[1] == "(未鑑定)":
                    pass
                else:
                    copyList.pop(i)
            data.stonesList = copyList
            data.gold += data.price
            del data.price
            systemDis0("売却可能な石をまとめ売りしました。")
            systemDis0("現在の所持金は %s です。" % data.gold)
        # カーソルが石のリストからはみ出さないようにします。
        data.cursor = min(data.cursor, max(len(data.stonesList) - 1, 0))
        data.attr = "browseStones"
        return data

    # ==============================
    # キーイベント
    # ==============================
    def inputA(self, data):
        if data.attr == "talkMerchant":
            data = self.browseBullets(data)
        return data
    def inputD(self, data):
        if data.attr == "talkMerchant":
            data = self.browseStones(data)
        return data
    def inputZ(self, data):
        if   data.attr == "browseBullets":
            data = self.checkBullet(data)
        elif data.attr == "checkBullet":
            data = self.buyBullet(data)
        elif data.attr == "browseStones":
            data = self.checkStone(data)
        elif data.attr == "checkStone" or data.attr == "checkAllStones":
            data = self.sellStone(data)
        return data
    def inputX(self, data):
        if   data.attr == "talkMerchant":
            data.attr = ""
        elif data.attr == "browseBullets":
            data = self.talkMerchant(data)
        elif data.attr == "checkBullet":
            data = self.browseBullets(data)
        elif data.attr == "browseStones":
            data = self.talkMerchant(data)
        elif data.attr == "checkStone" or data.attr == "checkAllStones":
            data = self.browseStones(data)
        return data
    def inputW(self, data):
        if data.attr == "browseBullets" and data.cursor != 0:
            data.cursor -= 1
        elif data.attr == "browseStones" and data.cursor != 0:
            data.cursor -= 1
        return data
    def inputS(self, data):
        if data.attr == "browseBullets" and data.cursor != (len(WithMerchant.saleList) - 1):
            data.cursor += 1
        elif data.attr == "browseStones" and data.cursor != (len(data.stonesList) - 1):
            data.cursor += 1
        return data
    def inputC(self, data):
        if   data.attr == "browseStones":
            data = self.checkAllStones(data)
        return data

