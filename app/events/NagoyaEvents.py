# !/usr/bin/env python
# coding: utf-8

# NagoyaEvent

from CommonFunctions import *
import Screen
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
            Screen.scene("貼り紙がある。「フィールドでは害獣に注意しましょう。」")
            # キー入力
            key  = Screen.ask("[w]進む [s]戻る [c]メニュー [save]セーブ", quit=True)
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

            Screen.scene("旅人のうわさ話が聞こえてくる。", random.choice(conversationsList))
            # キー入力
            key  = Screen.ask("[w]進む [s]戻る [c]メニュー [save]セーブ", quit=True)
            data = self.inputKey(key, data, ["w","s","c","save"])

    def event10(self, data):
        while 1:
            if data.m != 10:
                return data
            Screen.scene("道路標識がある。「この先20M、ナガクテ・フィールドへの小道アリ。」")
            # キー入力
            key  = Screen.ask("[w]進む [s]戻る [c]メニュー [save]セーブ", quit=True)
            data = self.inputKey(key, data, ["w","s","c","save"])

    def event20(self, data):
        while 1:
            if data.m != 20:
                return data
            Screen.scene("旅の商人がいる。「いらっしゃい」")
            # キー入力
            key  = Screen.ask("[w]進む [s]戻る [z]売買する")
            data = self.inputKey(key, data, ["w","s","z"])

    def event30(self, data):
        while 1:
            if data.m != 30:
                return data
            Screen.scene("ナガクテ・フィールドへの小道がある。")
            # キー入力
            key  = Screen.ask("[w]無視して進む [s]戻る [z]ナガクテ・フィールドへ這入る")
            data = self.inputKey(key, data, ["w","s","z"])

    def event40(self, data):
        while 1:
            if data.m != 40:
                return data
            Screen.scene("貼り紙がある。「この先10M、害獣の巣アリ。注意セヨ」")
            # キー入力
            key  = Screen.ask("[w]進む [s]戻る [c]メニュー [save]セーブ", quit=True)
            data = self.inputKey(key, data, ["w","s","c","save"])

    def event42(self, data):
        # 所持金5000以上でのみ出現
        if data.gold < 5000:
            return data

        data.attr = "Nagoya42"
        while 1:
            Screen.scene("ランダムイベント: そのへんの草むらが気になる…。")
            # キー入力
            key = Screen.ask("[z]調べる [x]そそくさと離れる")
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
            Screen.scene("武装馬車がいる。「ベースキャンプまで乗ってくかい?」")
            # キー入力
            key  = Screen.ask("[w]進む [s]戻る [z]乗る")
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

            Screen.scene("強力な害獣の巣だ。", "これ以上先へは進めない。")
            # キー入力
            key  = Screen.ask("[s]戻る [c]メニュー")
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
