# !/usr/bin/env python
# coding: utf-8

# SpecialEnemy ボス駆除処理を担当するメソッド集

from CommonFunctions import *
from InputKey        import *
from CreateStone     import *
import random
from GunFunctions    import *

class SpecialEnemy(InputKey):
    # ==============================
    # Python Nagoya 50M
    # 毎回弱点がかわり、hp5(弱点弾*2+普通弾)で駆除する。5/6の確率で倒せるってこと。
    # ダメージ表: 2-1 2-1 1-*
    # ==============================
    def shootPython(data):
        # 選択した弾の情報を得る
        bulletANDnum = data.bulletsList[data.cursor].split("@")
        bulletColor  = bulletANDnum[0].replace("弾", "")

        if bulletColor == data.pythonWeak:
            data.enHp -= (2 + addDamage(data))
            systemDis0(addMessageW(data))
        else:
            data.enHp -= (1 + addDamage(data))
            systemDis0(addMessageN(data))

        if data.enHp <= 0:
            # 相手のHPが0以下になったら駆除完了
            systemDis0("敵の大ヘビははじけ飛んだ。駆除を終了します。")
            systemDis0("自分の傷を手当しました。")

            # 賞品として5.0CMの石を入手
            nameANDcm = CreateStone.createStone("Nagoya").split("@")
            data.stonesList.append(nameANDcm[0] + "@5.0CM")
            systemDis0("大ヘビは何か石を吐き出した。")
            systemDis0("持ち物に %s 5.0CM を追加しました。" % nameANDcm[0])

            # troDataListに"Python"追加
            if not "Python" in data.troDataList:
                data.troDataList.append("Python")

            systemDis0("==============================")
            data.attr = ""
        else:
            # 相手が死んでないなら自分は1食らう
            data.myHp -= 1
            systemDis0("敵の大ヘビに締め付けられた。1ダメージを受けた。")

        return data

    # ==============================
    # Buffalo Nagakute 50M
    # 弱点は黒。弱点弾を2発うつと危機を感じて暴れられて死ぬ。
    # 普通弾を2発うつとナメて様子をみるのでそこから弱点弾2発うって殺す。hp6
    # ダメージ表: 2-1 2-2* やられパターン
    # ダメージ表: 1-1 1-様子見 2-1 2-*
    # ダメージ表: 1-1 2-1 1-1* やられパターン
    # ==============================
    def shootBuffalo(data):
        # 選択した弾の情報を得る
        bulletANDnum = data.bulletsList[data.cursor].split("@")
        bulletColor  = bulletANDnum[0].replace("弾", "")

        if bulletColor == data.dic["weak"]:
            data.his.append("weak")
            data.enHp -= (2 + addDamage(data))
            systemDis0(addMessageW(data))
        else:
            data.his.append("normal")
            data.enHp -= (1 + addDamage(data))
            systemDis0(addMessageN(data))

        if data.enHp <= 0:
            # 相手のHPが0以下になったら駆除完了
            systemDis0("敵の大スイギュウははじけ飛んだ。駆除を終了します。")
            systemDis0("自分の傷を手当しました。")

            # 賞品として5.0CMの石を入手
            nameANDcm = CreateStone.createStone("Nagakute").split("@")
            data.stonesList.append(nameANDcm[0] + "@5.0CM")
            systemDis0("大スイギュウは何か石を吐き出した。")
            systemDis0("持ち物に %s 5.0CM を追加しました。" % nameANDcm[0])

            # troDataListに"Buffalo"追加
            if not "Buffalo" in data.troDataList:
                data.troDataList.append("Buffalo")

            systemDis0("==============================")
            data.attr = ""
        else:
            if   len(data.his) == 1:
                # 1ループ目はふつうに1ダメージ食らう
                data.myHp -= 1
                systemDis0("敵の大スイギュウに突き上げられた。1ダメージを受けた。")
            else:
                if   (data.his[-1] == "weak") and (data.his[-2] == "weak"):
                    # 弱点弾を2発つづけて撃つと2ダメージ食らう
                    data.myHp -= 2
                    systemDis0("敵の大スイギュウは危機を感じて大暴れした。2ダメージを受けた。")
                elif (data.his[-1] == "normal") and (data.his[-2] == "normal"):
                    if (len(data.his) >= 3) and (data.his[-3] == "normal"):
                        # 普通弾を3発つづけて撃ったらふつうに1ダメージ(延々と普通弾撃ってもダメ)
                        data.myHp -= 1
                        systemDis0("敵の大スイギュウに突き上げられた。1ダメージを受けた。")
                    else:
                        # 普通弾を2発つづけて撃つとナメて行動しない
                        systemDis0("敵の大スイギュウはこちらをナメくさって行動しない。")
                else:
                    # ソレ以外はふつうに1ダメージ食らう
                    data.myHp -= 1
                    systemDis0("敵の大スイギュウに突き上げられた。1ダメージを受けた。")
        return data

    # ==============================
    # Robber Nagoya 42M
    # まず最初にランダムで抗体を打つ。その後は撃たれた弾の抗体を打つ。抗体を撃った属性は0ダメージとなる。
    # ==============================
    def shootRobber(data):
        # 選択した弾の情報を得る
        bulletANDnum = data.bulletsList[data.cursor].split("@")
        bulletColor  = bulletANDnum[0].replace("弾", "")

        if   len(data.anti) == 0:
            # 1ターン 最初の抗体を決める
            data.anti.append(random.choice(("赤", "青", "黒")))
            if bulletColor in data.anti:
                # 抗体の色に当てた場合ダメージは0
                data.enHp -= 0
                systemDis0("この弾はまったく効いていないようだ。0ダメージを与えた。")
                systemDis0("敵はニヤリと笑った。")
                data.his.append("no")
            else:
                # 他の色に当てた場合
                data.enHp -= (2 + addDamage(data))
                systemDis0(addMessageW(data))
                data.his.append("weak")
        elif len(data.his) == 1:
            # 抗体がいっこのとき
            if bulletColor in data.anti:
                # 抗体に当てた場合
                data.enHp -= 0
                systemDis0("この弾はまったく効いていないようだ。0ダメージを与えた。")
                systemDis0("敵はニヤリと笑った。")
                data.his.append("no")
            else:
                # 他の色に当てた場合
                data.enHp -= (2 + addDamage(data))
                systemDis0(addMessageW(data))
                data.his.append("weak")
        else:
            # 抗体が2つ以上のとき
            if bulletColor in data.anti:
                data.enHp -= 0
                systemDis0("この弾はまったく効いていないようだ。0ダメージを与えた。")
                systemDis0("敵はニヤリと笑った。")
                data.his.append("no")
            else:
                # 他の色に当てた場合は[0]の抗体を消して新たな抗体を足す
                data.enHp -= (2 + addDamage(data))
                systemDis0(addMessageW(data))
                data.his.append("weak")

        if data.enHp <= 0:
            # 相手のHPが0以下になったら駆除完了
            systemDis0("敵のニンゲンははじけ飛んだ。駆除を終了します。")
            systemDis0("自分の傷を手当しました。")

            # 賞品として5.0CMの石とお金を入手
            prizes = random.choice(SpecialEnemy.scorpionsList)
            data.stonesList.append(prizes[0] + "@5.0CM")
            data.gold += 2000
            systemDis0("強盗の死骸の荷から石とお金を見つけた。")
            systemDis0("持ち物に %s 5.0CM を追加しました。" % prizes[0])
            systemDis0("所持金に 2000 加えました。")

            # troDataListに"Robber"追加
            if not "Robber" in data.troDataList:
                data.troDataList.append("Robber")

            systemDis0("==============================")
            data.attr = ""
        else:
            if data.his[-1] == "weak":
                # このターン弱点弾を撃ったら敵は抗体を打つのでダメージなし
                systemDis0("敵はうめきつつ、なにか抗体のようなものを打った…。")
                if len(data.anti) >= 2:
                    data.anti.pop(0)
                data.anti.append(bulletColor)
            else:
                # でなければ普通に撃たれる
                data.myHp -= 1
                systemDis0("敵のニンゲンに撃ち抜かれた。1ダメージを受けた。")
            # 特殊な負けイベント
            if data.myHp <= 0:
                data.gold -= 2000
                systemDis0("よろめいた隙に、2000金奪われてしまった!")
        return data

    # ==============================
    # Scorpions Nagakute 40M
    # 出会ったら死ぬから、「あのへんはヤバイ」ってヒントを与えて、そのへんでは避けるようにする。
    # クリア報酬の猟銃マーク2で倒せる。
    # ダメージ表: 4-1 4-1 4*
    # ==============================
    scorpionsList = [
        "ドノマイド","イブル","エリファス","ドラレメ","イルザルシパル","ラポ","エショウクルット","テンラグ","エニラマウカ","ザポット",
        "エティルドナグゼラ","トシセマ","エニルチック","オディレプ","エティナズナット","エティカラム","アロコシルク","エダージュ","エターガ","エティロイ",
        ]

    def shootScorpions(data):
        # 選択した弾の情報を得る
        bulletANDnum = data.bulletsList[data.cursor].split("@")
        bulletColor  = bulletANDnum[0].replace("弾", "")

        if bulletColor == data.dic["weak"]:
            data.enHp -= (2 + addDamage(data))
            systemDis0(addMessageW(data))
        else:
            data.enHp -= (1 + addDamage(data))
            systemDis0(addMessageN(data))

        if data.enHp <= 0:
            # 相手のHPが0以下になったら駆除完了
            systemDis0("敵のサソリの群れははじけ飛び散った。駆除を終了します。")
            systemDis0("自分の傷を手当しました。")

            # 賞品として5.0CMの石を2つ入手
            prizes = random.sample(SpecialEnemy.scorpionsList, 2)
            data.stonesList.append(prizes[0] + "@5.0CM")
            data.stonesList.append(prizes[1] + "@5.0CM")
            systemDis0("サソリの死骸の下から石を見つけた。")
            systemDis0("持ち物に %s 5.0CM と %s 5.0CM を追加しました。" % (prizes[0], prizes[1]))

            # troDataListに"Scorpions"追加
            if not "Scorpions" in data.troDataList:
                data.troDataList.append("Scorpions")

            systemDis0("==============================")
            data.attr = ""
        else:
            # 相手が死んでないなら自分は1食らう
            data.myHp -= 1
            systemDis0("敵のサソリの群れにもみくちゃにされた。1ダメージを受けた。")

        return data


