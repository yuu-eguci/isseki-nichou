# !/usr/bin/env python
# coding: utf-8

# ==============================
# 文章出力関数
# 表示のしかた (画面の描き直しか追記か、 1 文字ずつ出すか) は Screen が決めます。
# ==============================
# このファイルは makePaths() より前に読み込まれるので、 Screen は関数の中で import します。
import sys

# 会話文を 1 文字ずつ出すとき (ISSEKI_TYPEWRITER=1) の間隔です。
messageInterval = 0.005

def systemDis0(statement):
    import Screen
    Screen.say(statement)

def systemDis(statement):
    import Screen
    Screen.say(statement)

# ==============================
# 文章出力関数(開発用) <ADMIN>がつく
# ==============================
def adminDis0(statement):
    print("<ADMIN>" + statement)
def adminDis(statement):
    print("<ADMIN>" + statement + "\n\n")

# ==============================
# あっちこっちディレクトリをいったりきたりするので、そのたびに相対インポートするのは大変
# なのでimport pathに全ディレクトリをあらかじめ登録しちゃう
# ==============================
import os

def makeDirs():
    dirs = []
    dirs.append(os.getcwd())
    for directory in dirs:
        files = os.listdir(directory)
        for f in files:
            path = directory + os.sep + f
            if os.path.isdir(path):
                dirs.append(path)
    return dirs

def makePaths():
    dirs = makeDirs()
    for directory in dirs:
        if directory in sys.path:
            # もう登録されてるパスならパス …いや狙ってないよ
            pass
        else:
            sys.path.append(directory)
            # sys.path.insert(0, directory)


if __name__ == "__main__":
    systemDis0("systemDis0のテストだよ")
    systemDis("同じくsystemDisのテストだよ")
