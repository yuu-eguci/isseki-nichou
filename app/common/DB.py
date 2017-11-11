# !/usr/bin/env python
# coding: utf-8

# DBのロードとセーブ

import sqlite3
from CommonFunctions import *
from Data            import *
from CreateStone     import *

class DB:
    # ==============================
    # DBのsavesテーブルのカラム情報を書いてね "カラム名":"初期値"
    # ==============================
    saveColumns = [
        {"id"     : ""},
        {"name"   : ""},
        {"field"  : "Nagoya"},
        {"m"      : 1},
        {"stones" : "クズ石@1.0CM"},
        {"guns"   : "汎用駆除銃@1"},
        # 自己レビューにより、弾薬とお金はもっとあっていいと出た。いっそモリモリ増やしてみる。1->50,0->1000
        {"bullets": "赤弾@50,青弾@50,黒弾@50"},
        {"gold"   : 1000},
        {"score"  : ""},
        {"trophy" : "|||"}, # trophyは (得た勲章のCSV)|||(勲章関係のデータ) というフォーマットで保存する
        ]

    # ==============================
    # でそれをいろんなふうに成形する関数たち
    # ==============================
    def columns2Csv(*withouts):
        # "id,name,field,m..."こういうのを作る
        # withoutsのリストに入ってるものは除く
        tempList = []
        for dic in DB.saveColumns:
            tempList.append(list(dic.keys())[0])
        for w in withouts:
            if w in tempList:
                tempList.remove(w)
        result = ",".join(tempList)
        return result

    def columns2List(*withouts):
        # ["id","name","field"...]こういうのを作る
        # withoutsのリストに入ってるものは除く
        result = []
        for dic in DB.saveColumns:
            result.append(list(dic.keys())[0])
        for w in withouts:
            if w in result:
                result.remove(w)
        return result

    def values2Tuple(*withouts):
        # ("Nagoya",1,""...)こういうのを作る
        # withoutsのリストに入ってるものは除く
        tempList1 = DB.columns2List(withouts)
        for w in withouts:
            if w in tempList1:
                tempList1.remove(w)
        tempList2 = []
        for t in tempList1:
            for dic in DB.saveColumns:
                if t == list(dic.keys())[0]:
                    tempList2.append(list(dic.values())[0])
        return tuple(tempList2)

    # ==============================
    # SELECTに使うassoc関数
    # ==============================
    def assoc(trash, columns=False):
        if columns == False:
            # columnsがFalse: SELECT * のとき
            col = DB.columns2List()
        else:
            # columnsにリストが: SELECT {特定のカラム} のとき
            col = columns
        rows = []
        for i in range(len(trash)):
            rows.append({})
            for j in range(len(trash[i])):
                rows[i][col[j]] = trash[i][j]
        return rows

    # ==============================
    # 新しくデータを作る 名前が重複してたらFalseを返し、ふつうに登録できたらTrueを返す
    # ==============================
    def makeData(inputName):
        connection = sqlite3.connect("app/isseki.sqlite3")
        cursor     = connection.cursor()

        # inputNameが重複していないかチェックする
        query      = "SELECT name FROM saves;"
        cursor.execute(query)
        trash      = cursor.fetchall()
        saves      = DB.assoc(trash, ["name"])
        for save in saves:
            if save["name"] == inputName:
                return False

        # 重複がないならまずnameだけ登録する
        query = ("INSERT INTO saves (name) VALUES (?);")
        cursor.execute(query, (inputName,))
        connection.commit()

        # クエリ用の "field=?,m=?,stones=?..." を作る
        csv1 = "=?,".join(DB.columns2List("id", "name")) + "=?"
        # 初期値でbindする用のタプルを作る
        tuple4Bind = DB.values2Tuple("id", "name") + (inputName,)

        # 初期値で登録する
        query = ("UPDATE saves SET " +
            "%s " % csv1 +
            "WHERE name=?;")
        cursor.execute(query, tuple4Bind)
        connection.commit()
        cursor.close()
        connection.close()
        systemDis0("新規データを作成しました。")
        return True

    # ==============================
    # ロードする 該当する名前のデータがあったらTrue、なければFalseを返す
    # ==============================
    def load(name):
        connection = sqlite3.connect("app/isseki.sqlite3")
        cursor     = connection.cursor()
        query      = "SELECT * FROM saves WHERE name=?;"
        cursor.execute(query, (name,))
        trash      = cursor.fetchall()
        cursor.close()
        connection.close()

        if trash == []:
            systemDis0("データが見つかりませんでした。")
            return False
        else:
            saves = DB.assoc(trash)
            # ロードが完了したら、それを記録装置インスタンスdataに保存する
            data  = Data(saves[0])
            systemDis0("ロードが完了しました。")
            return data

    # ==============================
    # セーブする 記録装置dataを受け取り、データをUPDATEする
    # ==============================
    def save(data):
        # stonesList,gunsList,bulletsListをcsvにする
        # data内では"stonesList"だけど、DBカラムでは"stones"だから新しい属性つくるよ
        data.stones  = ",".join(data.stonesList)
        data.guns    = ",".join(data.gunsList)
        data.bullets = ",".join(data.bulletsList)
        data.score   = ",".join(data.scoreList)
        data.trophies= ",".join(data.trophiesList)
        data.troData = ",".join(data.troDataList)

        # 余計な","が混入してるときのため、取り除き処理
        if data.stones.startswith(",")  : data.stones  = data.stones.lstrip(",")
        if data.guns.startswith(",")    : data.guns    = data.guns.lstrip(",")
        if data.bullets.startswith(",") : data.bullets = data.bullets.lstrip(",")
        if data.score.startswith(",")   : data.score   = data.score.lstrip(",")
        if data.trophies.startswith(","): data.trophies= data.trophies.lstrip(",")
        if data.troData.startswith(",") : data.troData = data.troData.lstrip(",")

        # trophyデータの成形
        data.trophy = data.trophies + "|||" + data.troData

        # DB接続開始する
        connection = sqlite3.connect("app/isseki.sqlite3")
        cursor     = connection.cursor()

        # クエリ用の "field=?,m=?,stones=?..." を作る
        csv1 = "=?,".join(DB.columns2List("id", "name")) + "=?"
        # id,name以外の値を順番通りにリストにする
        valuesList = []
        for column in DB.columns2List("id", "name"):
            valuesList.append(data.__dict__[column])
        tuple4Bind = tuple(valuesList) + (data.name,)

        # 更新する
        query = ("UPDATE saves SET " +
            "%s " % csv1 +
            "WHERE name=?;")
        cursor.execute(query, tuple4Bind)
        connection.commit()
        cursor.close()
        connection.close()

        systemDis0("セーブが完了しました。")

    # ==============================
    # 収集本レコードの作成 1からnumページまでのbooksレコードを作る
    # ==============================
    def addPage(data):
        # numは新たなページを追加するとき手動で増やしていく
        num = 2

        # DB接続開始する
        connection = sqlite3.connect("app/isseki.sqlite3")
        cursor     = connection.cursor()

        # 現在booksテーブルにあるページレコードの数
        query = "SELECT COUNT(page) FROM books WHERE save_id=?;"
        cursor.execute(query, (data.id,))
        now = cursor.fetchall()[0][0]

        # 不足レコードのINSERT now+1番目からnumまでのpageのレコードを作る
        for i in range(now+1, num+1):
            query = "INSERT INTO books (save_id, page) VALUES (?, ?);"
            cursor.execute(query, (data.id, i))
            connection.commit()
        cursor.close()
        connection.close()

        # ページ追加があったかどうかをreturnする なかったら0が返る
        return num - now

    # ==============================
    # 収集本のロード
    # ==============================
    def loadPage(data):
        # 指定されたsave_idとpageのレコードをbooksテーブルからひろってくる
        connection = sqlite3.connect("app/isseki.sqlite3")
        cursor     = connection.cursor()

        query = ("SELECT " +
            "column1," +
            "column2," +
            "column3," +
            "column4," +
            "column5," +
            "column6," +
            "column7," +
            "column8," +
            "column9," +
            "column10 " +
            "FROM books WHERE save_id=? AND page=?;")
        cursor.execute(query, (data.id, data.page))
        trash = cursor.fetchall()
        cursor.close()
        connection.close()

        # ちゃんとレコードがあるならディクショナリに成形する
        if trash != []:
            columns = [
                "column1",
                "column2",
                "column3",
                "column4",
                "column5",
                "column6",
                "column7",
                "column8",
                "column9",
                "column10",
                ]
            row = DB.assoc(trash, columns)[0]
        else:
            row = False

        return row

    # ==============================
    # DB.stones 名前をもとにpage,columnの値を得るディクショナリ
    # ==============================
    stones = {
        "ドノマイド":
            {"page":1, "column":1},
        "イブル":
            {"page":1, "column":2},
        "エリファス":
            {"page":1, "column":3},
        "ドラレメ":
            {"page":1, "column":4},
        "イルザルシパル":
            {"page":1, "column":5},
        "ラポ":
            {"page":1, "column":6},
        "エショウクルット":
            {"page":1, "column":7},
        "テンラグ":
            {"page":1, "column":8},
        "エニラマウカ":
            {"page":1, "column":9},
        "ザポット":
            {"page":1, "column":10},

        "エティルドナグゼラ":
            {"page":2, "column":1},
        "トシセマ":
            {"page":2, "column":2},
        "エニルチック":
            {"page":2, "column":3},
        "オディレプ":
            {"page":2, "column":4},
        "エティナズナット":
            {"page":2, "column":5},
        "エティカラム":
            {"page":2, "column":6},
        "アロコシルク":
            {"page":2, "column":7},
        "エダージュ":
            {"page":2, "column":8},
        "エターガ":
            {"page":2, "column":9},
        "エティロイ":
            {"page":2, "column":10},
    }

    # ==============================
    # 収集本への追加
    # ==============================
    def putInBook(data):
        # 対象石のpageとcolumnを特定する
        name   = data.target.split(" ")[0]
        size   = data.target.split(" ")[1]
        page   = DB.stones[name]["page"]
        column = "column" + str(DB.stones[name]["column"])

        # DB接続開始する
        connection = sqlite3.connect("app/isseki.sqlite3")
        cursor     = connection.cursor()

        # その部分にもともと入っているsizeを得る
        query = ("SELECT %s FROM books " % column +
            "WHERE save_id = ? AND page = ?;")
        cursor.execute(query, (data.id, page))
        pastSize = cursor.fetchall()[0][0]

        # UPDATE books SET <column>=<size> WHERE save_id=<data.id> AND page=<data.page>
        query = ("UPDATE books SET %s = ? " % column +
            "WHERE save_id = ? AND page = ?;")
        cursor.execute(query, (size, data.id, page))
        connection.commit()
        cursor.close()
        connection.close()

        # もともと入っていたものを返す
        return pastSize if pastSize else False

    # ==============================
    # booksテーブルレコードの取得
    # ==============================
    def loadPages4Score(data):
        connection = sqlite3.connect("app/isseki.sqlite3")
        cursor     = connection.cursor()

        query = ("SELECT " +
            "column1," +
            "column2," +
            "column3," +
            "column4," +
            "column5," +
            "column6," +
            "column7," +
            "column8," +
            "column9," +
            "column10 " +
            "FROM books WHERE save_id=? " +
            "ORDER BY page ASC;")
        cursor.execute(query, (data.id,))
        trash = cursor.fetchall()
        cursor.close()
        connection.close()

        # ちゃんとレコードがあるならディクショナリに成形する
        if trash != []:
            columns = [
                "column1",
                "column2",
                "column3",
                "column4",
                "column5",
                "column6",
                "column7",
                "column8",
                "column9",
                "column10",
                ]
            rows = DB.assoc(trash, columns)
        else:
            rows = False

        return rows

    # ==============================
    # クリア時に収集本をリセットする
    # ==============================
    def resetBook(data):
        # DB接続開始する
        connection = sqlite3.connect("app/isseki.sqlite3")
        cursor     = connection.cursor()

        # booksの、save_id=data.idのレコードを空欄にする
        query = ("UPDATE books SET " +
            "column1  = ''," +
            "column2  = ''," +
            "column3  = ''," +
            "column4  = ''," +
            "column5  = ''," +
            "column6  = ''," +
            "column7  = ''," +
            "column8  = ''," +
            "column9  = ''," +
            "column10 = '' " +
            "WHERE save_id = ?;"
            )
        cursor.execute(query, (data.id,))
        connection.commit()
        cursor.close()
        connection.close()


if __name__ == "__main__":
    print(DB.addPage(1))
