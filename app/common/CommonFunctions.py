# !/usr/bin/env python
# coding: utf-8

# ==============================
# 文章出力関数
# ==============================
import time, sys

# 1文字ずつちんたら表示したいときはTrueにしてね
systemDisSwitch = True

messageInterval = 0.005

def systemDis0(statement):
    stmt = list(statement)
    sys.stdout.write("<SYSTEM>")
    for st in stmt:
        sys.stdout.write(st)
        sys.stdout.flush()
        time.sleep(messageInterval)
    sys.stdout.write("\n")
    sys.stdout.flush()

def systemDis(statement):
    stmt = list(statement)
    sys.stdout.write("<SYSTEM>")
    for st in stmt:
        sys.stdout.write(st)
        sys.stdout.flush()
        time.sleep(messageInterval)
    sys.stdout.write("\n\n\n")
    sys.stdout.flush()

invInterval = 0.02

def invDis(statement):
    stmt = list(statement)
    sys.stdout.write("    ")
    for st in stmt:
        sys.stdout.write(st)
        sys.stdout.flush()
        time.sleep(invInterval)
    sys.stdout.write("\n")
    sys.stdout.flush()

# ==============================
# 文章出力関数(開発用) つまりちんたら出力しない
# ==============================
if systemDisSwitch == False:
    def systemDis0(statement):
        print("<SYSTEM>" + statement)
    def systemDis(statement):
        print("<SYSTEM>" + statement + "\n\n")
    def invDis(statement):
        print("    " + statement)

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
import sys, os

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
