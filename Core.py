# coding=utf-8
from Functions import *


def Merge(srt, ass):
    print(u"******start*******")
    cSrt = 0
    cAss = 0
    allAss = len(ass)
    allSrt = len(srt)
    suc = 0
    ig = 0
    while cAss < allAss:
        if ass[cAss][1] == -1 or ass[cAss][1] == -2:
            pass
            # print(u"***************预处理已忽略***********")
        else:
            flag = 0  # 是否匹配成功
            for x in range(cSrt, allSrt):
                if int(srt[x][1]) - int(ass[cAss][3]) > 40:  # ■■■■■此处修改两版本字幕同一句话时间轴允许偏差最大值（*BUG 默认 60秒）
                    break
                if ass[cAss][5].lower() == srt[x][3].lower() or Levenshtein(ass[cAss][5], srt[x][3]) > 70:
                    # ■■■■■此处修改两版本对白可认为是同义句所需相似度 默认 ：70（%）
                    ass[cAss][1] = x
                    cSrt = x + 1
                    if x + 1 >= allSrt:
                        x -= 1
                    flag = 1
                    break

            if flag == 0:
                # print("*******匹配失败 此行将被忽略**********")
                ass[cAss][1] = -1
                ig += 1
            else:
                # print("%+39s|%-39s" % (ass[cAss][5], srt[cSrt][3]))
                suc += 1
        cAss += 1
        if int(float(cAss) / allAss * 100) % 10 == 0:
            print(u"*******complete (%):" + str(int(float(cAss) / allAss * 100)))
    print(u"succeeded %d\nignored %d" % (suc, ig))
    print(u"finished")
    print(u"time shifting")
    offset = 0.0
    for x in ass:
        if x[1] != -1 and x[1] != -2:
            offset = srt[x[1]][1] - x[3]  # srt时间-ass时间
            x[3] += offset
            x[4] += offset
        else:
            x[3] += offset
            x[4] += offset
    print(u"finished")
    # 修正时间轴重叠
    for i in range(1, len(ass)):
        if ass[i][1] != -2 and ass[i - 1][1] != -2 and ass[i][3] < ass[i - 1][4] and ass[i - 1][4] - ass[i][3] < 1:
            # ■■■■重叠多少秒以内将被修正，默认：1（秒）
            ass[i][3] = ass[i - 1][4]
    return ass
