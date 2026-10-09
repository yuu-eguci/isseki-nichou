# !/usr/bin/env python
# coding: utf-8

# NagakuteEvent

from CommonFunctions import *
import Screen
from InputKey        import *
from RandomEvents    import *
from WithMerchant    import *
import random
from KickEnemy       import *
from WithHorse       import *

class NagakuteEvents(InputKey):
    # イベントを起こすm数をディクショナリにしておく
    mList = {
        "1" : "self.event1" ,    # 「名古屋フィールドへの小道」
        "10": "self.event10",    # 「商人 石の買い取りと弾の販売」
        "20": "self.event20",    # 「適当な会話」
        "30": "self.event30",    # 「この先10M、ボスじゃないんだけどちょっと強い奴いるから気をつけて」
        "40": "self.event40",    # 「ちょっと強い害獣」
        "45": "self.event45",    # 馬車
        "50": "self.event50",    # 「フィールドボス 倒すと5.0CMの石をなんかくれる」
    }

    # ==============================
    # いまのmに固定イベントがあったら対応するメソッドを実行する
    # ==============================
    def eventJunction(self, data):
        if str(data.m) in NagakuteEvents.mList:
            data = eval(NagakuteEvents.mList[str(data.m)])(data)
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
            Screen.scene("ナゴヤ・フィールドへの小道がある。")
            # キー入力
            key  = Screen.ask("[w]無視して進む [s]戻る [z]ナゴヤ・フィールドへ這入る")
            data = self.inputKey(key, data, ["w","s","z"])

    def event10(self, data):
        while 1:
            if data.m != 10:
                return data

            # 適当な会話
            conversationsList = [
                "「怪しい天気だがね、予報じゃ雨は降らないって話だよ」",
                "「ウワサじゃ大蛇はよく大きな石を丸呑みするとか」",
                "「ナゴヤのほうにはこのへんにゃ無い石が発見できるそうだ」",
                "「ナガクテの奥の方ではなるだけ探索を避けたほうがよさそうだね」",
                "「ナガクテ・フィールドの大ボスの弱点は、黒弾らしいぜ」",
                ]

            Screen.scene("旅人のうわさ話が聞こえてくる。", random.choice(conversationsList))
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
            Screen.scene("旅人たちの話が聞こえてくる。", "「この先のほうで、好戦的な害獣が目撃されているそうだ。あんたも気をつけな」", "「出遭いそうになったらそそくさと離れた方がいいぜ」")
            # キー入力
            key  = Screen.ask("[w]進む [s]戻る [c]メニュー [save]セーブ", quit=True)
            data = self.inputKey(key, data, ["w","s","c","save"])

    def event40(self, data):
        data.attr = "Nagakute40"
        while 1:
            Screen.scene("ランダムイベント: そのへんの草むらが気になる…。")
            # キー入力
            key = Screen.ask("[z]調べる [x]そそくさと離れる")
            data = self.inputKey(key, data, ["z","x"])
            if   data.attr == "":
                return data
            elif data.attr == "scorpions":
                break
        battle = KickEnemy()
        data.enemy = "Scorpions"
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
        data.enemy = "Buffalo"
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
    def inputZ(self, data):
        if   data.m == 1:
            data.m     = 30
            data.field = "Nagoya"
            systemDis0("ナゴヤ・フィールドへ這入りました。")
        elif data.m == 20:
            merchant = WithMerchant()
            data = merchant.talkMerchant(data)
            del merchant
        elif data.m == 40:
            data.attr = "scorpions"
        elif data.m == 45:
            horse = WithHorse()
            data = horse.talkHorse(data)
            del horse
        return data
    def inputX(self, data):
        if   data.m == 40:
            data.attr = ""
        return data