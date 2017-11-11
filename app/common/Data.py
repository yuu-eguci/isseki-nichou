# !/usr/bin/env python
# coding: utf-8

# データ記録装置

class Data:
    def __init__(self, dic):
        # ==============================
        # {"name":"aaa", "field":"Nagoya"...} って感じで飛んでくる
        # DBのsavesテーブルのカラムを増やすときはここも増やしてね
        # ==============================
            self.id          = dic["id"]
            self.name        = dic["name"]
            self.field       = dic["field"]
            # self.mが-1以下のときは0にしとく(キャンプ内セーブだったら0からスタート)
            self.m           = dic["m"] if dic["m"] >= 0 else 0
            self.stonesList  = dic["stones"].split(",")
            self.gunsList    = dic["guns"].split(",")
            self.bulletsList = dic["bullets"].split(",")
            self.gold        = dic["gold"]
            self.scoreList   = dic["score"].split(",")

            # trophyは"|||"でわけて、前半を得た勲章のリスト、後半を勲章関係のデータのリストで取得する
            troANDdata       = dic["trophy"].split("|||")
            self.trophiesList= troANDdata[0].split(",")
            self.troDataList = troANDdata[1].split(",")

            # リストデータは、中身がひとつかつ空文字列だったら空リストにする
            self.stonesList  = [] if (len(self.stonesList)  == 1) and (self.stonesList[0]  == "") else self.stonesList
            self.gunsList    = [] if (len(self.gunsList)    == 1) and (self.gunsList[0]    == "") else self.gunsList
            self.bulletsList = [] if (len(self.bulletsList) == 1) and (self.bulletsList[0] == "") else self.bulletsList
            self.scoreList   = [] if (len(self.scoreList)   == 1) and (self.scoreList[0]   == "") else self.scoreList
            self.trophiesList= [] if (len(self.trophiesList)== 1) and (self.trophiesList[0]== "") else self.trophiesList
            self.troDataList = [] if (len(self.troDataList) == 1) and (self.troDataList[0] == "") else self.troDataList

if __name__ == "__main__":
    # これはただのテスト用データなんで気にしないでねー
    testDic = {
        "id"     :5,
        "name"   :"Jack",
        "field"  :"Sapporo",
        "m"      :50,
        "stones" :"ガーネット@1.9CM,石@(未鑑定)@ターコイズ@3.5CM,石@(未鑑定)@ガーネット@2.7CM",
        "guns"   :"汎用駆除銃@1",
        "bullets":"赤弾@1,青弾@2,黒弾@3",
        "gold"   :1024,
        }
    data       = Data(testDic)
    print(data.field, data.m)
    data.field = "Hakodate"
    data.m    += 600
    print(data.field, data.m)