# coding=utf-8


# the clean-ish way
a4 = [65,122,97,110,111,118,105,99]
a5 = [0x42,0x03,0x65,0x01,0x20,0x04,0x52,0x01,0x65,0x05,0x61,0x09,0x64,0x02,0x79,0x06]
f = []
for i in range(0, len(a5)-1, 2):
    if a5[i] & 1:
        f.append(a4[i/2] + a5[i+1])
    else:
        f.append(a4[i/2] - a5[i+1])
print("GH18{%s}" % "".join([chr(x ^ y) for x,y in zip(f, [20,41,20,62,55,82,49,67])]))


# the real way
print("GH18{%s}" % "".join([chr(((f - c) ^ x) & 0xff) if m & 1 == 0 else chr(((f + c) ^ x) & 0xff) for f, m, c, x in zip([65,122,97,110,111,118,105,99], [0x42,0x65,0x20,0x52,0x65,0x61,0x64,0x79], [3,1,4,1,5,9,2,6], [20,41,20,62,55,82,49,67])]))
