
from random import randint

d = 4
f = "A"
flag = bytearray()
flag.extend(f)
m = "Z"
mask = bytearray()
mask.extend(f)

def bytes_to_bits(bytes_array):
    bits = []
    for o in bytes_array:
        for i in range(8):
            bits.append((o >> i) & 1)
    return bits

def xor(l):
    res = 0
    for i in l:
        res ^= i
    return res

def simulate_leaks(flag, mask, probes, hook=None):
    """
    Simulate the value on the wires probed when computing the bitwise AND
    between the flag (constant) and a constant mask. This function is
    called just after the user gives his probes.
    """
    leaks = []
    masked_flag_bits = []

    print("flag", flag, bytes_to_bits(flag))
    print("mask", mask, bytes_to_bits(mask))

    for a, b in zip(bytes_to_bits(flag), bytes_to_bits(mask)):
        c, leak = secure_and(a, b, d, probes, hook)
        masked_flag_bits.append(c)
        leaks.append(leak)

    return leaks

def sharing(s, d):
    if s not in [0, 1]:
        raise ValueError("Only binary value accepted")
    """
    Make a sharing of `s` into `d`+1 shares such that the XOR of the `d`+1
    shares is equal to `s`.
    """

    s_sharing = []
    for i in range(d):
        s_sharing.append(randint(0,1))
    s_sharing.append(xor(s_sharing)^s)
    
    return s_sharing

def secure_and(a, b, d, probes, hook=None):
    """
    Mimic a hardware circuit "securely" computing `a`&`b` and return the 
    result as well as the information that an attacker would have by
    probing on the wires defined in `probes`. The maximum number of probes
    allowed is `d`.
    """
    if len(probes) > d:
        raise ValueError('Too many probes')

    leaks = {}

    if hook is not None:
        print("\n---")
        print("before sharing a: %r" % a)
        print("before sharing b: %r" % b)

    a = sharing(a, d)
    b = sharing(b, d)
    if hook == "x":
        print("after sharing a: %r" % a)
        print("after sharing b: %r" % b)
    else:
        if "a" in hook:
            print("a: %r" % a)
        if "b" in hook:
            print("b: %r" % b)

    # a and b leaks
    for i in range(d+1):
        wire = 'a_{}'.format(i)
        if wire in probes:
            leaks[wire] = a[i]
        wire = 'b_{}'.format(i)
        if wire in probes:
            leaks[wire] = b[i]
    
    alpha = []
    for i in range(len(a)):
        alpha.append([])
        for j in range(len(b)):
            alpha[-1].append(a[i] & b[j])
            wire = 'alpha_{},{}'.format(i, j)
            if wire in probes:
                leaks[wire] = alpha[i][j]
    if hook == "x" or "p" in hook:
        print("alpha: %r" % alpha)

    ## d-compression algorithm
    c_sharing = []
    for i in range(d+1):
        tmp = 0
        for j in range(d+1):
            if j != d:
                x = ((j%d)+i)%(d+1)
                if hook == "x" or "z" in hook:
                    print("c_%d,%d = tmp ^ alpha[%d][%d] = %d ^ %d = %d" % (i, j, x, i, tmp, alpha[x][i], tmp ^ alpha[x][i]))
                tmp ^= alpha[x][i]
            else:
                x = ((j%d)+i)%(d+1)
                y = (i+1)%(d+1)
                if hook == "x" or "z" in hook:
                    print("c_%d,%d = tmp ^ alpha[%d][%d] = %d ^ %d = %d" % (i, j, x, y, tmp, alpha[x][y], tmp ^ alpha[x][y]))
                tmp ^= alpha[x][y]
            wire = 'c_{},{}'.format(i, j)
            if wire in probes:
                leaks[wire] = tmp
        c_sharing.append(tmp)
    if hook == "x" or "s" in hook:
        print("c_sharing: %r" % c_sharing)
            
    ## Canonical decoder
    c = xor(c_sharing)
    if hook == "x" or "c" in hook:
        print("c: %r" % c)

    if len(leaks) > len(probes):
        raise Exception("Something went wrong with the leaks")

    return c, leaks


def play(flag, mask):
    import os

    flag = bytearray()
    flag.extend("Z")
    mask = bytearray()
    mask.extend("B")
    ex = ["q", "exit", "quit"]
    while True:
        try:
            print("\n\n=== ")
            cmd = raw_input("What do we do? ")
            if cmd in ex:
                break
            if cmd in ["cls", "clear", "reset"]:
                os.system("reset||cls")
            if cmd.startswith("flag"):
                flag = bytearray()
                flag.extend(cmd.split("flag ")[1])
            elif cmd.startswith("mask"):
                mask = bytearray()
                mask.extend(cmd.split("mask ")[1])
            elif cmd.startswith("bits"):
                print(bytes_to_bits(flag), len(bytes_to_bits(maks)))
            elif cmd.startswith("sharing"):
                tmp = bytes_to_bits(flag)
                for i, a, b in zip(xrange(len(tmp)), tmp, bytes_to_bits(mask)):
                    print(i, a, sharing(a, d), b, sharing(b, d))
            elif cmd.startswith("probe"):
                probes = cmd.split("probe ")[1]
                print(simulate_leaks(flag, mask, probes))
            elif cmd.startswith("dbg"):
                # x to debug all
                # z to debug c_sharing tables
                # p to debug alpha
                # a to debug a
                # b to debug b
                # s to debug c_sharing
                # c to debug c
                print(simulate_leaks(flag, mask, ["b_4", "alpha_3,4", "c_4,3"], cmd.split("dbg ")[1]))
                print(bytes_to_bits(flag))
        except KeyboardInterrupt:
            cmd = raw_input("\nDo we quit? ")
            if cmd in ex + ["y", "yes"]:
                break
        except IndexError:
            print("Error in the cmd")


play(flag, mask)
# nc chohzatheeghahwoesus.challenge.grehack.fr 2341
# a = a[0] ^ a[1] ^ a[2] ^ a[3] ^ a[4]
# b = b[0] ^ b[1] ^ b[2] ^ b[3] ^ b[4]
# flag[0] & mask[0] = c[0] = ((a[0] ^ b[0]) ^ c_sharing[0]) ^ ((a[1] ^ b[1]) ^ c_sharing[1]) ... ^ ((a[4] ^ b[4]) ^ c_sharing[4])
# flag[X] & mask[X] = c[X] = ((a[0] ^ b[0]) ^ c_sharing[0]) ^ ((a[1] ^ b[1]) ^ c_sharing[1]) ... ^ ((a[4] ^ b[4]) ^ c_sharing[4])