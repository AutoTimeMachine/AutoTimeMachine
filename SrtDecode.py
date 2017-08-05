# coding=utf-8
import codecs, os, io, re
import chardet
from Functions import *


def ReadSrt(filename):  # srt格式化读取，结果格式：[序号，起始秒，结束秒，内容去除特效标签与SDH的内容]的list
    bytes2 = min(32, os.path.getsize(filename))
    raw = open(filename, 'rb').read(bytes2)
    if raw.startswith(codecs.BOM_UTF8):
        encoding = 'utf-8-sig'
    else:
        result = chardet.detect(raw)
        encoding = result['encoding']

    srtFile = io.open(filename, 'r', encoding=encoding)

    res = []
    cur = []
    i = 0
    for line in srtFile:
        if line == "\n":
            res.append(cur)
            cur = []
            i = 0
        else:
            i += 1
            if i == 1:
                line = line.replace('\n', '')
                cur.append(int(line))
            elif i == 2:
                s = re.findall(r'\d+:\d+:\d+,\d+', line)
                t1 = int(s[0][0:2]) * 3600 + int(s[0][3:5]) * 60 + int(s[0][6:8]) + float(int(s[0][9:12])) / 1000.0
                t2 = int(s[1][0:2]) * 3600 + int(s[1][3:5]) * 60 + int(s[1][6:8]) + float(int(s[1][9:12])) / 1000.0
                cur.append(t1)
                cur.append(t2)
            elif i == 3:
                line = re.sub(r'(\([^\)]+\))', '', line) #匹配(asdfg)
                line = re.sub(r'<([^>]+)>', '', line)#匹配<asdfg>
                line = re.sub(r'\[([^\]]+)\]', '', line)#匹配[asdfg]
                line = line.replace('\n', ' ')
                line = line[0:len(line) - 1]
                cur.append(line)
            else:
                line = re.sub(r'(\([^\)]+\))', '', line)
                line = re.sub(r'<([^>]+)>', '', line)
                line = re.sub(r'\[([^\]]+)\]', '', line)
                line = line.replace('\n', ' ')
                line = line[0:len(line) - 1]
                cur[3] = cur[3] + ' ' + line

    res.append(cur)
    while [] in res:
        res.remove([])
    srtFile.close()
    for x in res[:]:  # 删除纯SDH内容行
        if ENcheck2(x[3]) == 0:
            res.remove(x)
    i = 0
    for x in res:  # 序号重排
        i += 1
        x[0] = i
    # for i in res:
    #     print(i)
    return res

# ReadSrt("test.srt")
