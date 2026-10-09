# !/usr/bin/env python
# coding: utf-8

# ==============================
# 画面の表示とキー入力の窓口です。
# 端末では「ヘッダー・場面・最近の出来事・使えるキー」を入力のたびに描き直します。
# パイプや TERM=dumb 、 ISSEKI_PLAIN=1 のときは、制御文字を使わずに 1 行ずつ追記します。
# ==============================
import os, sys, shutil, time, unicodedata
from collections import deque

AREAS = {"Nagoya": "ナゴヤ・エリア", "Nagakute": "ナガクテ・エリア"}

current = None      # いま遊んでいるセーブデータ (DB.load で設定されます)
saved   = None      # 最後にセーブ / ロードしたときの中身
body    = []        # 次の入力までに出された場面と一覧の行
log     = deque(maxlen=40)
lastScene = None    # 追記表示で最後に出した場面 (同じ場面を繰り返さないためです)
lastHeader = None   # 追記表示で最後に出したヘッダー
repeats = 1         # 最後の出来事が続けて何回出たか

def reset():
    global current, saved, lastScene, lastHeader, repeats
    current, saved, lastScene, lastHeader, repeats = None, None, None, None, 1
    body.clear()
    log.clear()

def isPlain():
    return (os.environ.get("ISSEKI_PLAIN") == "1" or os.environ.get("TERM") == "dumb"
            or not sys.stdout.isatty())

# ==============================
# 表示幅 (全角は 2 桁) の計算
# ==============================
def charWidth(ch):
    return 2 if unicodedata.east_asian_width(ch) in "WF" else 1

def width(text):
    return sum(charWidth(ch) for ch in text)

def wrap(text, cols):
    lines, line = [], ""
    for ch in text:
        if line and width(line + ch) > cols:
            lines.append(line)
            line = ""
        line += ch
    return lines + [line]

def wrapKeys(keys, cols):
    # キーの説明は [ の前で折り返し、どのキーも欠けないようにします。
    lines = []
    for item in keys.replace(" [", "\n[").split("\n"):
        if lines and width(lines[-1] + " " + item) <= cols:
            lines[-1] += " " + item
        else:
            lines.extend(wrap(item, cols))
    return lines

def pad(text, cols):
    return text + " " * (cols - width(text))

def table(rows, cursor=None):
    # 列を表示幅で揃え、カーソル行に > を付けます。
    widths = [max(width(row[i]) for row in rows if len(row) > i) for i in range(max(map(len, rows), default=0))]
    lines = []
    for i, row in enumerate(rows):
        cells = [pad(cell, widths[j]) for j, cell in enumerate(row)]
        lines.append(("> " if i == cursor else "  ") + "  ".join(cells).rstrip())
    return lines

def bar(now, most):
    now = max(now, 0)
    return "[%s%s] %d/%d" % ("#" * now, "." * (most - now), now, most)

# ==============================
# セーブ状態
# ==============================
def signature(data):
    # セーブされる中身だけを比べます。カーソルやメニューの位置は含めません。
    # キャンプや収集本では m が負になりますが、ロードすると 0 になるので同じものとして扱います。
    return (data.field, max(data.m, 0), data.gold,
            tuple(data.stonesList), tuple(data.gunsList), tuple(data.bulletsList),
            tuple(data.scoreList), tuple(data.trophiesList), tuple(data.troDataList))

def markSaved(data):
    global current, saved
    current, saved = data, signature(data)

def isDirty():
    return current is not None and signature(current) != saved

def header():
    if current is None:
        return "一石二鳥"
    if current.m < 0:
        place = "キャンプ"
    else:
        place = "%s %d M" % (AREAS.get(current.field, current.field), current.m)
    return "%s | 所持金 %s | 石 %d | %s" % (
        place, current.gold, len(current.stonesList), "未保存" if isDirty() else "保存済み")

# ==============================
# 出力
# ==============================
def say(text):
    # 出来事やセリフです。
    global repeats
    if isPlain():
        typewrite(text)
    elif log and log[-1] in (text, "%s (x%d)" % (text, repeats)):
        # 同じ出来事が続いたときは、回数を付けて 1 行にまとめます。
        repeats += 1
        log[-1] = "%s (x%d)" % (text, repeats)
    else:
        repeats = 1
        log.append(text)

def typewrite(text):
    # ISSEKI_TYPEWRITER=1 のとき、会話文だけ 1 文字ずつ表示します。
    import CommonFunctions
    if os.environ.get("ISSEKI_TYPEWRITER") == "1" and "「" in text and sys.stdout.isatty():
        for ch in text:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(CommonFunctions.messageInterval)
        sys.stdout.write("\n")
    else:
        print(text)

def scene(*lines):
    # いまの場面です。追記表示では、前と同じ場面は出し直しません。
    global lastScene
    if isPlain():
        if lines != lastScene:
            for line in lines:
                print(line)
        lastScene = lines
    else:
        body.extend(lines)

def rows(lines):
    # 一覧です。カーソルが動くたびに出し直します。
    # 一覧を出したあとは別の画面とみなし、次の場面は同じ文でも出し直します。
    global lastScene
    if isPlain():
        lastScene = None
        for line in lines:
            print(line)
    else:
        body.extend(lines)

def frame(sceneLines, logLines, keys, cols, height):
    # 端末 1 画面分の行を作ります。最後の 1 行は入力欄に残します。
    # 狭い端末でも保存状態が欠けないよう、ヘッダーは折り返します。
    limit = max(height - 1, 1)
    top   = wrap(header(), cols) + [""]
    foot  = [""] + wrapKeys(keys, cols)
    if len(top) + len(foot) > limit:
        # 低すぎる端末では空行を省き、キーを優先して残します。
        foot = foot[1:][-limit:]
        top  = top[:-1][:limit - len(foot)]
    room = limit - len(top) - len(foot)
    main = [part for line in sceneLines for part in wrap(line, cols)]
    if len(main) > room:
        # 長い一覧は、カーソル行 (> で始まる行) が見える位置までずらします。
        cursor = next((i for i, line in enumerate(main) if line.startswith("> ")), 0)
        start  = min(max(cursor - room + 1, 0), len(main) - room)
        main   = main[start:start + room]
    news = [part for line in logLines for part in wrap(line, cols)]
    news = news[len(news) - max(room - len(main) - 1, 0):] if room - len(main) > 1 else []
    return top + main + ([""] + news if news else []) + foot

def read():
    # パイプから読んだ入力は画面に出ないので、追記表示のときは記録として出し直します。
    key = input()
    if isPlain() and not sys.stdin.isatty():
        print(key)
    return key

def ask(keys, quit=False):
    # 使えるキーを表示して 1 行読みます。 quit=True の画面では quit で終了できます。
    if quit:
        keys += " [quit]終了"
    while 1:
        show(keys)
        key = read()
        if not (quit and key == "quit"):
            return key
        if not isDirty():
            raise SystemExit(0)
        say("セーブしていない進行があります。セーブせずに終了すると、前回のセーブから再開になります。")
        while 1:
            show("[z]セーブせずに終了 [x]ゲームに戻る")
            answer = read()
            if answer.lower() == "z":
                raise SystemExit(0)
            if answer.lower() == "x":
                break

def show(keys):
    global lastHeader
    if isPlain():
        # 追記表示では、現在地などが変わったときだけヘッダーを出します。
        if current is not None and header() != lastHeader:
            lastHeader = header()
            print("-- %s --" % lastHeader)
        print(keys)
        sys.stdout.write("> ")
        sys.stdout.flush()
        return
    size  = shutil.get_terminal_size()
    lines = frame(body, list(log), keys, size.columns, size.lines)
    body.clear()
    # 画面を消さずに上から上書きするので、ちらつきません。
    out = "\x1b[H" + "".join("%s\x1b[K\n" % line for line in lines)
    sys.stdout.write(out.replace(lines[0], "\x1b[7m%s\x1b[0m" % lines[0], 1) + "\x1b[J> ")
    sys.stdout.flush()
