# coding=utf-8
import codecs, os, io, re
import chardet
from operator import itemgetter
from Functions import *


def ReadAssHead(filename):  # 读取ass文件头部信息
    bytes2 = min(32, os.path.getsize(filename))
    raw = open(filename, 'rb').read(bytes2)
    if raw.startswith(codecs.BOM_UTF8):
        encoding = 'utf-8-sig'
    else:
        result = chardet.detect(raw)
        encoding = result['encoding']

    assFile = io.open(filename, 'r', encoding=encoding)
    x = assFile.read()
    y = """Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"""
    x = x[0:x.find(y) + len(y) + 1]  # 只保留头
    x = x.replace("[Script Info]", u"[Script Info]\n; Synced by AutoTimeMachine 1.0\n; https://github.com/AutoTimeMachine/AutoTimeMachine")
    # print(x)
    return x


def ReadAss(filename):  # 读取ass文件  返回： 序号1（1,2,3...），序号2（待定 0:未定 -1:忽略），风格样式，开始时间，结束时间，英文部分，原文
    res = []
    cur = []
    bytes2 = min(32, os.path.getsize(filename))
    raw = open(filename, 'rb').read(bytes2)
    if raw.startswith(codecs.BOM_UTF8):
        encoding = 'utf-8-sig'
    else:
        result = chardet.detect(raw)
        encoding = result['encoding']

    assFile = io.open(filename, 'r', encoding=encoding)
    x = assFile.read()
    y = """Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"""

    x = x[x.find(y) + len(y) + 1:len(x)]  # 只保留正文
    # print x
    lines = x.split("\n")
    i = 0
    for line in lines:
        if len(line) > 8:
            i += 1
            cur = []
            temp = line.split(",", 9)
            cur.append(i)
            cur.append(0)
            cur.append(temp[3])
            cur.append(inttime(temp[1]))
            cur.append(inttime(temp[2]))
            en = temp[9]
            en = re.sub(r'(\([^\)]+\))', '', en)  # 匹配(asdfg)
            en = re.sub(r'<([^>]+)>', '', en)  # 匹配<asdfg>
            en = re.sub(r'\[([^\]]+)\]', '', en)  # 匹配[asdfg]
            en = re.sub(r'\{([^\}]+)\}', '', en)  # 匹配{asdfg} ass标签
            if not ("\\N" in en) and (ENcheck(en) > 50):
                zhPattern = re.compile(u'[\u4e00-\u9fa5]+')  # 检测中文
                match = zhPattern.search(en)
                if match:
                    en = ""
                en = en
            elif ("\\N" in en) and en.count("\\N") > 1:
                zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
                t = en.split("\\N")
                en = ""
                for tt in t:
                    match = zhPattern.search(tt)
                    if ENcheck(tt) > 60 and (not match):
                        en = en + "\\N" + tt
                if en[0:2] == "\\N":
                    en = en[2:]
            elif ("\\N" in en) and en.count("\\N") == 1:
                t = en.split("\\N")
                en = t[1]
                zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
                match = zhPattern.search(en)
                if match:
                    en = ""
            else:
                en = ""
            cur.append(en)
            if en == "":
                cur[1] = -2
            cur.append(temp[9])
            res.append(cur)
    res.sort(key=itemgetter(3), reverse=False)
    i = 0
    for x in res:
        i += 1
        x[0] = i
        # print(x)
    return res
