# !/usr/bin/env python
# coding: utf-8

# NagakuteEvent

from CommonFunctions import *
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
            systemDis0("ナゴヤ・フィールドへの小道がある。")
            systemDis("'w'で無視して進む 's'で戻る 'z'でナゴヤ・フィールドへ這入る。")
            # キー入力
            key  = input()
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

            systemDis0("旅人のうわさ話が聞こえてくる。")
            systemDis0(random.choice(conversationsList))
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
            systemDis0("旅人たちの話が聞こえてくる。")
            systemDis0("「この先のほうで、好戦的な害獣が目撃されているそうだ。あんたも気をつけな」")
            systemDis0("「出遭いそうになったらそそくさと離れた方がいいぜ」")
            systemDis("'w'で進む 's'で戻る 'c'でメニューを開く 'save'と入力するとセーブできます。")
            # キー入力
            key  = input()
            data = self.inputKey(key, data, ["w","s","c","save"])

    def event40(self, data):
        data.attr = "Nagakute40"
        while 1:
            systemDis0("ランダムイベント: そのへんの草むらが気になる…。")
            systemDis("'z'で調べる 'x'でそそくさと離れる。")
            # キー入力
            key = input()
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
            systemDis0("武装馬車がいる。「ベースキャンプまで乗ってくかい?」")
            systemDis("'w'で進む 's'で戻る 'z'で乗る。")
            # キー入力
            key  = input()
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