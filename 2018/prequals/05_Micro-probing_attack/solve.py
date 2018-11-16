# coding=utf-8


from pwn import *
import binascii


# Micro-probing attack
bin_flag = [None] * (42 * 8)
r = remote("chohzatheeghahwoesus.challenge.grehack.fr", 2341)
r.recv()
r.sendline("0")
r.recv()
r.sendline("b_4;alpha_3,4;c_4,3")
attempt = 0
max_attempt = 100000
while True:
    leaks = r.recvuntil("-------------------------------------------")
    for i, leak in enumerate(leaks.splitlines()[:-1]):
        # {'b_4': 1, 'alpha_3,4': 1, 'c_4,3': 0}
        l = eval(leak)
        if bin_flag[i] is None:
            if l["b_4"] == 1:
                bin_flag[i] = l["alpha_3,4"] ^ l["c_4,3"]
    if None not in bin_flag:
        break
    r.recv()
    attempt += 1
    if attempt >= max_attempt:
        break
    r.sendline("1")
flag = ""
for i in range(0, len(bin_flag), 8):
    flag += binascii.unhexlify("%x" % int('0b%s' % ("".join(map(str, bin_flag[i:i+8][::-1]))), 2))
print(flag)