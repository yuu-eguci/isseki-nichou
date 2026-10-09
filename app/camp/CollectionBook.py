# !/usr/bin/env python
# coding: utf-8

# CollectionBook

from CommonFunctions import *
import Screen
from InputKey        import *
from DB              import *
import datetime
from types           import SimpleNamespace
from Trophy          import *

class CollectionBook(InputKey):
    # ==============================
    # 本を開く self.mが-3ならここへ来る
    # ==============================
    def openBook(self, data):
        data.m    = -3
        data.attr = "openBook"
        # 不足ページの追加
        if DB.addPage(data):
            systemDis0("収集本の更新が行われました。")

        # コンプリートしてたら分岐する
        if self.checkComplete(data):
            while 1:
                Screen.scene("声をかけられた。「石をコンプリートしたようね。集計する?」", self.collectedLine(data))

                # キー入力
                key = Screen.ask("[番号]ページを見る [c]手持ちの石を収める [z]収集本のスコアを集計してもらう [x]戻る")

                # 数字と文字の分岐
                if key.isdecimal() and len(key) <= 3:
                    data.page = int(key)
                    data = self.openPage(data)
                else:
                    data = self.inputKey(key, data, ["c","x","z"])

                if data.m != -3:
                    return data
        else:
            while 1:
                Screen.scene("収集本を手に取りました。「丁寧に扱ってよね」", self.collectedLine(data))

                # キー入力
                key = Screen.ask("[番号]ページを見る [c]手持ちの石を収める [x]戻る")

                # 数字と文字の分岐
                if key.isdecimal() and len(key) <= 3:
                    data.page = int(key)
                    data = self.openPage(data)
                else:
                    data = self.inputKey(key, data, ["c","x"])

                if data.m != -3:
                    return data

    # ==============================
    # 収集した種類の数 (全ページ分) の表示
    # ==============================
    def collectedLine(self, data):
        count = 0
        for i in range(len(CollectionBook.pagesList)):
            columnList = DB.loadPage(SimpleNamespace(id=data.id, page=i + 1))
            if columnList:
                count += len([cm for cm in columnList.values() if cm])
        total = sum(len(names) for names in CollectionBook.pagesList)
        return "収集 %d/%d 種" % (count, total)

    # 収集本の表示用リスト インデックスがページ数 並び順がカラム順
    pagesList = [
        ["ドノマイド","イブル","エリファス","ドラレメ","イルザルシパル","ラポ","エショウクルット","テンラグ","エニラマウカ","ザポット"],
        ["エティルドナグゼラ","トシセマ","エニルチック","オディレプ","エティナズナット","エティカラム","アロコシルク","エダージュ","エターガ","エティロイ"],
        ]

    # ==============================
    # 指定ページの収集具合を表示する
    # ==============================
    def openPage(self, data):
        data.attr = "openPage"
        # そもそもそのページあるかどうか
        columnList = DB.loadPage(data)

        if columnList == False:
            systemDis0("そのページはありません。")
            data.attr = "openBook"
            return data
        else:
            while 1:
                Screen.scene("%sページを開きました。" % data.page)
                cells = []

                pageList = CollectionBook.pagesList[data.page - 1]
                for i in range(0, 10):
                    # 収集済みなら
                    cm = columnList["column" + str(i + 1)]
                    cm = cm if cm else ""
                    if cm:
                        collected = "★収集済み"
                    else:
                        collected = "未収集"

                    # 収集ページの表示
                    cells.append(["%02d" % (i + 1), pageList[i], collected, cm])
                Screen.rows(Screen.table(cells))


                # キー入力
                key = Screen.ask("[番号]ページを見る [c]手持ちの石を収める [x]戻る")

                # 数字と文字の分岐
                if key.isdecimal() and len(key) <= 3:
                    data.page = int(key)
                    data = self.openPage(data)
                else:
                    data = self.inputKey(key, data, ["c","x"])

                if data.attr != "openPage":
                    return data

    # ==============================
    # 石カバンを見る
    # ==============================
    def browseStones4Collect(self, data):
        data.attr = "browseStones4Collect"
        # カーソルの初期化
        data.cursor = 0
        while 1:
            # 石のリストを作る
            Screen.rows(Screen.table([stone.split("@")[:2] for stone in data.stonesList], data.cursor))

            # キー入力
            key = Screen.ask("[w/s]石を選ぶ [z]選んだ石を収める [x]戻る")
            data = self.inputKey(key, data, ["w","s","z","x"])

            if data.attr != "browseStones4Collect":
                return data

    # ==============================
    # 石を収める
    # ==============================
    def collectStone(self, data):
        # 石がひとつもないときは何もせずに戻ります。
        if len(data.stonesList) == 0:
            systemDis0("石がひとつもありません。")
            return data

        # "宝石名 サイズ"を作る
        nameANDcm   = data.stonesList[data.cursor].split("@")
        data.target = "%s %s" % (nameANDcm[0], nameANDcm[1])

        # 未鑑定品だった場合収集不可
        if nameANDcm[1] == "(未鑑定)":
            systemDis0("未鑑定品は収められない。「そもそも、なんだこれ?」")
            data.attr = "browseStones4Collect"
            return data

        # クズ石を収めようとした場合
        if nameANDcm[0] == "クズ石":
            systemDis0("クズ石は収められない。「それはいらないわ」")
            data.attr = "browseStones4Collect"
            return data

        # 鑑定済みの石ならDB.putInBookへ
        pastSize = DB.putInBook(data)
        systemDis0("%s を収集本に収めました。" % data.target)

        # もともとなんか入ってたときはそれをstonesListに追加する
        if pastSize:
            pastStone = nameANDcm[0] + "@" + pastSize
            data.stonesList.append(pastStone)
            systemDis0("収集本に入っていた %s をカバンに戻しました。" % (nameANDcm[0] + " " + pastSize))

        # いま収めたものをstonesListから削除
        data.stonesList.pop(data.cursor)

        # カーソルが石のリストからはみ出さないようにします。
        data.cursor = min(data.cursor, max(len(data.stonesList) - 1, 0))

        # ついでにメインデータのセーブを行う
        DB.save(data)

        return data

    # ==============================
    # 全部そろったらスコア集計コマンドを足す
    # ==============================
    def checkComplete(self, data):
        # とりあえずbooksのレコードをぶっこ抜いてみましょうか
        rows = DB.loadPages4Score(data)

        # 中身が全部埋まってるかどうかのチェック
        complete = True
        if rows:
            for page in rows:
                for i in range(10):
                    size = page["column" + str(i+1)]
                    size = float(size.replace("CM", "")) if size else 0
                    if size == 0:
                        complete = False
            return complete
        else:
            systemDis0("収集本にページがありません。")
            return False

    # ==============================
    # コレクションブックのスコア集計
    # ==============================
    def calcScore(self, data):
        # とりあえずbooksのレコードをぶっこ抜いてみましょうか
        rows = DB.loadPages4Score(data)

        # column1はsize*500, 2と3はsize*300, ソレ以外はsize*100
        score = 0
        if rows:
            for page in rows:
                for i in range(10):
                    size = page["column" + str(i+1)]
                    size = float(size.replace("CM", "")) if size else 0
                    if i == 0:
                        score += size * 500
                    if 1 <= i <= 2:
                        score += size * 300
                    else:
                        score += size * 100
            return score
        else:
            systemDis0("収集本にページがありません。")
            return False

    # ==============================
    # スコアを表示し、クリアーするかどうか選択する
    # ==============================
    def ending(self, data):
        data.attr = "ending"
        data.tmpScore = round(self.calcScore(data))

        # スコアによって台詞を変える
        if   data.tmpScore < 6000:
            scoreLine = "まあこんなものかしらね"
        elif data.tmpScore < 15000:
            scoreLine = "これはたいしたものね"
        elif data.tmpScore < 18999:
            scoreLine = "これ以上の結果はそうないでしょうね"
        elif data.tmpScore == 19000:
            scoreLine = "素晴らしいわね…最高の結果よ"

        while 1:
            Screen.scene("「集計結果は %s よ。%s」" % (data.tmpScore, scoreLine), "望むなら結果を記録し、ここを出ることができます。")

            # キー入力
            key = Screen.ask("[z]ここを出る [x]戻る")
            data = self.inputKey(key, data, ["z","x"])

            if data.attr != "ending":
                return data

    # ==============================
    # クリアと二周目処理
    # ==============================
    def clear(self, data):
        data.attr = "clear"

        systemDis0("ここを出ました。「これでアナタたちは自由の身よ」")
        systemDis0("それを聞きつけた商人が祝いの品をキャンプへ送ってきたが、行き違いになってしまったようだ…。")

        # scoreに日付を加えてscoreListに追加
        d = datetime.datetime.today()
        data.scoreList.append(str(data.tmpScore) + "|" + d.strftime("%Y.%m.%d."))

        # 周回数を使って猟銃生成
        clearNum = len(data.scoreList)
        newGun = "猟銃%sマーク%s@1" % (data.name, str(clearNum))
        data.gunsList.append(newGun)
        systemDis0("持ち物に %s を追加しました。" % newGun.split("@")[0])

        # 勲章を追加する 点数が19000なら極めクリアーの勲章も追加する
        if not "クリアー" in data.trophiesList:
            data.trophiesList.append("クリアー")
            systemDis0("勲章「クリアー」を取得しました。勲章はフィールドで'q'と入力すると閲覧できます。")
        if (data.tmpScore == 19000) and not ("極めクリアー" in data.trophiesList):
            data.trophiesList.append("極めクリアー")
            systemDis0("勲章「極めクリアー」を取得しました。勲章はフィールドで'q'と入力すると閲覧できます。")

        # 居場所をリセット
        data.m     = 1
        data.field = "Nagoya"

        # 収集本をリセットする
        DB.resetBook(data)

        # セーブする
        DB.save(data)

        systemDis0("クリアおめでとうございます。あなたのスコアは %s でした。" % data.scoreList[-1].split("|")[0])
        systemDis0("そして、新たなあなたがやってくる……")

        # 勲章をコンプしてたらコンプリートメソッドを出す
        if len(data.trophiesList) >= len(Trophy.trophiesList):
            data = self.completeGame(data)

        return data

    # ==============================
    # 全勲章コンプリート
    # ==============================
    def completeGame(self, data):
        data.attr = "completeGame"
        while 1:
            Screen.scene(
                "★★★★★★★★★★★★★★★★★★★★★★",
                "       You completed the Game!         ",
                "   Thank you very much for playing!    ",
                "★★★★★★★★★★★★★★★★★★★★★★")

            # キー入力
            key = Screen.ask("[z]「いえいえどういたしまして。」")
            data = self.inputKey(key, data, ["z"])

            if data.attr != "completeGame":
                return data

    # ==============================
    # キーイベント
    # ==============================
    def inputC(self, data):
        data = self.browseStones4Collect(data)
        return data
    def inputZ(self, data):
        if   data.attr == "browseStones4Collect":
            data = self.collectStone(data)
        elif data.attr == "openBook":
            data = self.ending(data)
        elif data.attr == "ending":
            data = self.clear(data)
        elif data.attr == "completeGame":
            data.attr = "clear"
        return data
    def inputX(self, data):
        if   data.attr == "openBook" or data.attr == "openPage":
            data.m = -1
            data.attr = ""
        elif data.attr == "browseStones4Collect":
            data = self.openBook(data)
        elif data.attr == "ending":
            data = self.openBook(data)
        return data
    def inputW(self, data):
        if   data.attr == "browseStones4Collect" and data.cursor != 0:
            data.cursor -= 1
        return data
    def inputS(self, data):
        if   data.attr == "browseStones4Collect" and data.cursor != (len(data.stonesList) - 1):
            data.cursor += 1
        return data
