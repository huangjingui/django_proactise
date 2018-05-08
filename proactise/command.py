#-*- coding:utf-8 -*-

import sys,os,hashlib

def hash(str):

    m = hashlib.md5()

    m.update(str.encode("utf8"))

    return m.hexdigest()
