# coding=utf-8


def f1(flag):
    y = flag[8]
    x = flag[7]
    flag[7] = flag[5]
    flag[5] = y
    flag[8] = flag[6]
    flag[6] = x
    flag[6] ^= 0x34
    return flag


def f2(flag):
    tmp = flag[7]
    while True:
        if tmp < flag[5]:
            break
        flag[6] += 1
        tmp -= 1
    return flag


def f3(flag):
    x = flag[8]
    while True:
        flag[5] -= 1
        x -= 1
        if x == ord('0'):
            break
    return flag


def f4(flag):
    x = flag[8]
    y = flag[7]
    flag[8] = flag[5]
    flag[5] = x
    flag[7] = flag[6]
    flag[6] = y
    return flag


def f5(flag):
    flag[5] ^= 0x1a
    flag[6] ^= 0x79
    flag[7] ^= 0x46
    flag[8] ^= 0x7c
    return flag


flag = map(ord, "GH18{....}")
flag = f5(flag)
flag = f4(flag)
flag = f3(flag)
flag = f2(flag)
print(["".join(map(chr, flag))])
