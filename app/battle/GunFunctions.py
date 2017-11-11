# !/usr/bin/env python
# coding: utf-8

# ==============================
# 武器の種類によってダメージ補正を作る関数
# ==============================
def addDamage(data):
    gunName = data.gunsList[0].split("@")[0]
    if gunName.startswith("猟銃"):
        # クリア報酬の猟銃を装備中だったら、末尾の数字に1を足した数を追加する
        return int(gunName[-1]) + 1
    else:
        return 0

# ==============================
# 武器の種類によってメッセージを作る関数 Nが普通弾のとき、Gが弱点弾のとき Normal,Weak
# ==============================
def addMessageN(data):
    if data.gunsList[0].startswith("猟銃"):
        # クリア報酬の猟銃を装備中だったら
        damage = 1 + addDamage(data)
        return "この弾はほどほどに効いているようだ。さらに猟銃が威力を上げた。%sダメージを与えた。" % damage
    else:
        return "この弾はほどほどに効いているようだ。1ダメージを与えた。"

def addMessageW(data):
    if data.gunsList[0].startswith("猟銃"):
        # クリア報酬の猟銃を装備中だったら
        damage = 2 + addDamage(data)
        return "この弾はよく効いているようだ。さらに猟銃が威力を上げた。%sダメージを与えた。" % damage
    else:
        return "この弾はよく効いているようだ。2ダメージを与えた。"



