# !/usr/bin/env python
# coding: utf-8

# KickEnemy 駆除を担当するクラス

from CommonFunctions import *
from InputKey        import *
from SpecialEnemy    import *
import random
from GunFunctions    import *
from Trophy          import *

class KickEnemy(InputKey):
    # ==============================
    # 害獣の情報
    # 緑-赤, 黄-青, 白-黒 がそれぞれ弱点
    # ==============================
    weakList = ["赤", "青", "黒"]

    enemies = {
        "Alligator":{"name":"ワニ", "hp":3, "weak":"赤", "field":"Nagoya", "event":"normal", "attack":"咬みつかれた"},
        "Hornet"   :{"name":"ハチ", "hp":3, "weak":"青", "field":"Nagoya", "event":"normal", "attack":"突き刺された"},
        "Robber"   :{"name":"ニンゲン", "hp":6, "weak":"", "field":"Nagoya", "event":"boss", "attack":"撃ち抜かれた"},
        "Python"   :{"name":"大ヘビ", "hp":5, "weak":"", "field":"Nagoya", "event":"boss", "attack":"締め付けられた"},

        "Tarantula":{"name":"クモ", "hp":3, "weak":"黒", "field":"Nagakute", "event":"normal", "attack":"千切られた"},
        "Leopard"  :{"name":"ヒョウ", "hp":3, "weak":"青", "field":"Nagakute", "event":"normal", "attack":"噛みつかれた"},
        "Scorpions":{"name":"サソリの群れ", "hp":10, "weak":"赤", "field":"Nagakute", "event":"boss", "attack":"もみくちゃにされた"},
        "Buffalo"  :{"name":"大スイギュウ", "hp":6, "weak":"黒", "field":"Nagakute", "event":"boss", "attack":"突き上げられた"},
    }

    # ==============================
    # 引数に敵の名前を受け取り、戦闘を展開する 呼び出すときはdata.enemyを指定してね
    # ==============================
    def kickEnemy(self, data):
        dic = KickEnemy.enemies[data.enemy]
        data.attr = "kickEnemy"
        data.cursor = 0

        # 初期hpの設定
        data.myHp = 3
        data.enHp = dic["hp"]

        # ボス敵は「遭遇時に毎回弱点がかわる」「ダメージの履歴を参照する」などメソッド外の情報を必要とするので、そのへんをdataへ記録
        data.dic = dic
        data.his = []
        data.anti = []
        data.pythonWeak = random.choice(KickEnemy.weakList)

        systemDis0("%s に襲われた! 「%s駆除しよう」" % (dic["name"], ("慎重に" if dic["event"] != "normal" else "")))

        while 1:
            systemDis0("==============================")
            systemDis0("敵:%s 残りHP:%s" % (dic["name"], data.enHp))
            systemDis0("自分残りHP:%s" % data.myHp)
            systemDis0("使用する弾薬を選んでください。使用銃:%s" % data.gunsList[0].split("@")[0])

            # 弾薬のリストを作る
            i = 0
            for bullet in data.bulletsList:
                nameANDnum = bullet.split("@")
                tmp = "==>" if data.cursor == i else ""
                invDis("%s %s *%s" % (tmp, nameANDnum[0], nameANDnum[1]))
                i += 1

            systemDis("上下(w,s)で弾薬を選ぶ 'z'で攻撃する 'x'で諦めます。")

            key = input()
            data = self.inputKey(key, data, ["w","s","z","x"])

            if data.attr != "kickEnemy":
                data = self.checkBossTro(data)
                return data

    # ==============================
    # ダメージ処理
    # ==============================
    def shootEnemy(self, data):
        # 選択した弾の情報を得る
        bulletANDnum = data.bulletsList[data.cursor].split("@")
        bulletColor  = bulletANDnum[0].replace("弾", "")

        if int(bulletANDnum[1]) <= 0:
            # 選択した弾が残弾0ならreturnする
            systemDis0("その弾の手持ちがありません。")
            return data
        else:
            # その弾をひとつ減らす
            data.bulletsList[data.cursor] = bulletANDnum[0] + "@" + str(int(bulletANDnum[1]) - 1)

        # normal以外が相手だったら専用のメソッドへ
        dic = KickEnemy.enemies[data.enemy]
        if KickEnemy.enemies[data.enemy]["event"] == "boss":
            data = eval("SpecialEnemy.shoot" + data.enemy)(data)
        else:
            ### 相手がnormal敵だったときの処理 ###
            # 選択した弾と敵のweakが一致したら2、でなければ1をdata.enHpから引く
            dic = KickEnemy.enemies[data.enemy]
            if bulletColor == dic["weak"]:
                data.enHp -= (2 + addDamage(data))
                systemDis0(addMessageW(data))
            else:
                data.enHp -= (1 + addDamage(data))
                systemDis0(addMessageN(data))

            if data.enHp <= 0:
                # 相手のHPが0以下になったら駆除完了
                systemDis0("敵の%sははじけ飛んだ。駆除を終了します。" % dic["name"])
                systemDis0("自分の傷を手当しました。")
                systemDis0("==============================")
                data.attr = ""
            else:
                # 相手が死んでないなら自分は1食らう
                data.myHp -= 1
                systemDis0("敵の%sに%s。1ダメージを受けた。" % (dic["name"], dic["attack"]))

        # 死んだら
        if data.myHp <= 0:
            systemDis0("深手を負った。あなたは半狂乱で逃げ出しました。")
            systemDis0("気づけば石カバンの中身を失い、キャンプに戻っていました。")
            systemDis0("==============================")
            data.stonesList = []
            data.m = -1
            data.attr = ""

        return data

    # ==============================
    # 諦める(石をぶちまけて逃走)
    # ==============================
    def giveUp(self, data):
        data.attr = "giveUp"

        while 1:
            systemDis0("==============================")
            systemDis0("石カバンを投げつけて逃走することができます。")
            systemDis0("手持ちの石をすべて失いますがよろしいですか?")
            systemDis("'z'でよろしい 'x'でやめます。")

            # キー入力
            key = input()
            data = self.inputKey(key, data, ["z","x"])

            if data.attr != "giveUp":
                return data

    # ==============================
    # 「ボス殲滅完了」の判定
    # ==============================
    def checkBossTro(self, data):
        flag = (
            ("Python"    in data.troDataList) and
            ("Robber"    in data.troDataList) and
            ("Scorpions" in data.troDataList) and
            ("Buffalo"   in data.troDataList)
            )
        if flag and not ("ボス殲滅完了" in data.trophiesList):
            data.trophiesList.append("ボス殲滅完了")
            systemDis0("勲章「ボス殲滅完了」を取得しました。勲章はフィールドで'q'と入力すると閲覧できます。")
        return data

    # ==============================
    # キーイベント
    # ==============================
    def inputW(self, data):
        if   data.cursor != 0:
            data.cursor -= 1
        return data
    def inputS(self, data):
        if   data.cursor != (len(data.bulletsList) - 1):
            data.cursor += 1
        return data
    def inputZ(self, data):
        if   data.attr == "kickEnemy":
            data = self.shootEnemy(data)
        elif data.attr == "giveUp":
            data.stonesList = []
            data.m -= 1
            data.attr = ""
            systemDis0("逃走に成功しましたが、石をすべて失いました。")
            systemDis0("==============================")
        return data
    def inputX(self, data):
        if   data.attr == "kickEnemy":
            data = self.giveUp(data)
        elif data.attr == "giveUp":
            data.attr = "kickEnemy"
        return data
