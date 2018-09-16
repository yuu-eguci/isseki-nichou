# !/usr/bin/env python
# coding: utf-8

# NagoyaEvent

from CommonFunctions import *
from InputKey        import *
from RandomEvents    import *
from WithMerchant    import *
from KickEnemy       import *
from WithHorse       import *

class NagoyaEvents(InputKey):
    # イベントを起こすm数をディクショナリにしておく
    mList = {
        "1" : "self.event1" ,    # 「フィールドでは害獣に注意しましょう」
        "5" : "self.event5" ,    # うわさ話
        "10": "self.event10",    # 「この先20M長久手フィールドへの道アリ」
        "20": "self.event20",    # 「商人 石の買い取りと弾の販売」
        "30": "self.event30",    # 「長久手フィールドへの小道」
        "40": "self.event40",    # 「この先10Mボスいるから気をつけて」
        "42": "self.event42",    # 強盗
        "45": "self.event45",    # 馬車
        "50": "self.event50",    # 「フィールドボス 倒すと5.0CMの石をなんかくれる」
    }

    # ==============================
    # いまのmに固定イベントがあったら対応するメソッドを実行する
    # ==============================
    def eventJunction(self, data):
        if str(data.m) in NagoyaEvents.mList:
            data = eval(NagoyaEvents.mList[str(data.m)])(data)
        else:
            rEvent = RandomEvents()
            data = rEvent.randomEvent(data)
        return data

    # ==============================
    # イベント郡
    # ==============================
    def event1(self, data):
        while 1:
            if data.m != 1:
                return data
            systemDis0("貼り紙がある。「フィールドでは害獣に注意しましょう。」")
            systemDis("'w'で進む 's'で戻る 'c'でメニューを開く 'save'と入力するとセーブできます。")
            # キー入力
            key  = input()
            data = self.inputKey(key, data, ["w","s","c","save"])

    def event5(self, data):
        while 1:
            if data.m != 5:
                return data

            # 適当な会話
            conversationsList = [
                "「フィールドを進みすぎたら、45M地点にいる馬車を利用しなよ。お金はかかるけど」",
                "「ナゴヤ・フィールドの大ボスの弱点は、毎度変わるそうだぜ」",
                "「ナガクテのほうにはこのへんにゃ無い石が発見できるそうだ」",
                "「あまり大金をもってフィールドの奥のほうを歩かないほうがいいぜ、強盗が出るって話だ」",
                ]

            systemDis0("旅人のうわさ話が聞こえてくる。")
            systemDis0(random.choice(conversationsList))
            systemDis("'w'で進む 's'で戻る 'c'でメニューを開く 'save'と入力するとセーブできます。")
            # キー入力
            key  = input()
            data = self.inputKey(key, data, ["w","s","c","save"])

    def event10(self, data):
        while 1:
            if data.m != 10:
                return data
            systemDis0("道路標識がある。「この先20M、ナガクテ・フィールドへの小道アリ。」")
            systemDis("'w'で進む 's'で戻る 'c'でメニューを開く 'save'と入力するとセーブできます。")
            # キー入力
            key  = input()
            data = self.inputKey(key, data, ["w","s","c","save"])

    def event20(self, data):
        while 1:
            if data.m != 20:
                return data
            systemDis0("旅の商人がいる。「いらっしゃい」")
            systemDis("'w'で進む 's'で戻る 'z'で売買をします。")
            # キー入力
            key  = input()
            data = self.inputKey(key, data, ["w","s","z"])

    def event30(self, data):
        while 1:
            if data.m != 30:
                return data
            systemDis0("ナガクテ・フィールドへの小道がある。")
            systemDis("'w'で無視して進む 's'で戻る 'z'でナガクテ・フィールドへ這入る。")
            # キー入力
            key  = input()
            data = self.inputKey(key, data, ["w","s","z"])

    def event40(self, data):
        while 1:
            if data.m != 40:
                return data
            systemDis0("貼り紙がある。「この先10M、害獣の巣アリ。注意セヨ」")
            systemDis("'w'で進む 's'で戻る 'c'でメニューを開く 'save'と入力するとセーブできます。")
            # キー入力
            key  = input()
            data = self.inputKey(key, data, ["w","s","c","save"])

    def event42(self, data):
        # 所持金5000以上でのみ出現
        if data.gold < 5000:
            return data

        data.attr = "Nagoya42"
        while 1:
            systemDis0("ランダムイベント: そのへんの草むらが気になる…。")
            systemDis("'z'で調べる 'x'でそそくさと離れる。")
            # キー入力
            key = input()
            data = self.inputKey(key, data, ["z","x"])
            if   data.attr == "":
                return data
            elif data.attr == "robber":
                break
        systemDis0("悪人面の強盗に出遭ってしまった。「クク、カモが財布を背負って来たな」")
        systemDis0("強盗はこちらの銃を見て、なにか抗体のようなものを打った…。")
        battle = KickEnemy()
        data.enemy = "Robber"
        data = battle.kickEnemy(data)
        del battle
        return data

    def event45(self, data):
        while 1:
            if data.m != 45:
                return data
            systemDis0("武装馬車がいる。「ベースキャンプまで乗ってくかい?」")
            systemDis("'w'で進む 's'で戻る 'z'で乗る。")
            # キー入力
            key  = input()
            data = self.inputKey(key, data, ["w","s","z"])

    def event50(self, data):
        systemDis0("強力な害獣の巣だ。")
        battle = KickEnemy()
        data.enemy = "Python"
        data = battle.kickEnemy(data)
        del battle

        while 1:
            if data.m != 50:
                return data

            systemDis0("強力な害獣の巣だ。")
            systemDis0("これ以上先へは進めない。")
            systemDis("'s'で戻る 'c'でメニューを開きます。")
            # キー入力
            key  = input()
            data = self.inputKey(key, data, ["s","c"])

    # ==============================
    # キーイベント
    # ==============================
    def inputW(self, data):
        systemDis0("1M進んだ。")
        data.m += 1
        return data
    def inputS(self, data):
        systemDis0("1M戻った。")
        data.m -= 1
        return data
    def inputC(self, data):
        inventory = Inventory()
        data = inventory.menu(data)
        del inventory
        return data
    def inputZ(self, data):
        if   data.m == 20:
            merchant = WithMerchant()
            data = merchant.talkMerchant(data)
            del merchant
        elif data.m == 30:
            data.m     = 1
            data.field = "Nagakute"
            systemDis0("ナガクテ・フィールドへ這入りました。")
        elif data.m == 42:
            data.attr = "robber"
        elif data.m == 45:
            horse = WithHorse()
            data = horse.talkHorse(data)
            del horse
        return data
    def inputX(self, data):
        if   data.m == 42:
            data.attr = ""
        return data
