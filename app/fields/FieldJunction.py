# !/usr/bin/env python
# coding: utf-8

# ==============================
# フィールドを追加したら、ここへも追加すること
# ==============================
from Camp          import *
from NagoyaField   import *
from NagakuteField import *

class FieldJunction:
    # ==============================
    # data.fieldの値をもとにField分岐を行う
    # 記録装置dataを渡し、返り値はField内で更新されたdata
    # ==============================
    def fieldJunction(data):
        while 1:
            # mが-1ならキャンプへ、ソレ以外ならfieldに記載されたフィールドへ
            if data.m == -1:
                field = Camp(data)
            else:
                field = eval(data.field + "Field")(data)
            data  = field.fieldMain(data)
            del field

if __name__ == "__main__":
    pass



