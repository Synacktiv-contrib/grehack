from random import randint

d = 4

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

def simulate_leaks(flag, mask, probes):
    """
    Simulate the value on the wires probed when computing the bitwise AND
    between the flag (constant) and a constant mask. This function is
    called just after the user gives his probes.
    """
    leaks = []
    masked_flag_bits = []

    for a, b in zip(bytes_to_bits(flag), bytes_to_bits(mask)):
        c, leak = secure_and(a, b, d, probes)
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

def secure_and(a, b, d, probes):
    """
    Mimic a hardware circuit "securely" computing `a`&`b` and return the 
    result as well as the information that an attacker would have by
    probing on the wires defined in `probes`. The maximum number of probes
    allowed is `d`.
    """
    if len(probes) > d:
        raise ValueError('Too many probes')

    leaks = {}

    a = sharing(a, d)
    b = sharing(b, d)

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

    ## d-compression algorithm
    c_sharing = []
    for i in range(d+1):
        tmp = 0
        for j in range(d+1):
            if j != d:
                tmp ^= alpha[((j%d)+i)%(d+1)][i]
            else:
                tmp ^= alpha[((j%d)+i)%(d+1)][(i+1)%(d+1)]
            wire = 'c_{},{}'.format(i, j)
            if wire in probes:
                leaks[wire] = tmp
        c_sharing.append(tmp)
            
    ## Canonical decoder
    c = xor(c_sharing)

    if len(leaks) > len(probes):
        raise Exception("Something went wrong with the leaks")

    return c, leaks

