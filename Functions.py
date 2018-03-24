# coding=utf-8

# 字符相似度比较
def Levenshtein(s, t):
    s = s.lower()
    t = t.lower()
    len_s = len(s)
    len_t = len(t)

    temp = [[0 for i in range(0, len_t + 1)] for j in range(len_s + 1)]
    # print(temp)
    # 将第一行和第一列初始化 0，1，2，3，。。。
    for i in range(len_s + 1):
        temp[i][0] = i
    for i in range(len_t + 1):
        temp[0][i] = i
    # 更新矩阵
    for i in range(1, len_s + 1):
        for j in range(1, len_t + 1):
            if s[i - 1] == t[j - 1]:
                flag = 0
            else:
                flag = 1
            temp[i][j] = min(temp[i - 1][j - 1] + flag,
                             temp[i][j - 1] + 1, temp[i - 1][j] + 1)

    return int(100 - temp[len_s][len_t] / float(max(len(s), len(t))) * 100)


# 英语比例检查
def ENcheck(s):
    if len(s) == 0:
        return 0
    i = 0
    for x in s:
        if ('a' <= x <= 'z') or ('A' <= x <= 'Z'):
            i += 1
    return int(100.0 * float(i) / float(len(s)))


def ENcheck2(s):
    i = 0
    for x in s:
        if ('a' <= x <= 'z') or ('A' <= x <= 'Z'):
            i += 1
    return i


def inttime(s):
    return int(s[0:1]) * 3600 + int(s[2:4]) * 60 + int(s[5:7]) + float(int(s[8:10]) / 100.0)


def strtime(t):
    mil = int((t - int(t)) * 100) % 100
    mil = u"%02d" % mil
    sec = int(t) % 60
    minute = (int(t) // 60) % 3600
    hour = int(t) // 3600
    return u"%d:%02d:%02d.%s" % (hour, minute, sec, mil)

