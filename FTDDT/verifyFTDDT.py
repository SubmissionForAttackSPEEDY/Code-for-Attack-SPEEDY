from SboxTool import SboxTool

S = [0x08,0x00,0x09,0x03,0x38,0x10,0x29,0x13,0x0c,0x0d,0x04,0x07,0x30,0x01,0x20,0x23,
                        0x1a,0x12,0x18,0x32,0x3e,0x16,0x2c,0x36,0x1c,0x1d,0x14,0x37,0x34,0x05,0x24,0x27,
                        0x02,0x06,0x0b,0x0f,0x33,0x17,0x21,0x15,0x0a,0x1b,0x0e,0x1f,0x31,0x11,0x25,0x35,
                        0x22,0x26,0x2a,0x2e,0x3a,0x1e,0x28,0x3c,0x2b,0x3b,0x2f,0x3f,0x39,0x19,0x2d,0x3d ]

Speedy_Sbox = SboxTool(S, 6)

Speedy_Sbox.DDTcompute()

DDT = Speedy_Sbox.DDT

def BitToSet(bitInput):
    # x0 means the LSB
    x0 = bitInput & 1
    x1 = (bitInput >> 1) & 1
    x2 = (bitInput >> 2) & 1
    x3 = (bitInput >> 3) & 1
    x4 = (bitInput >> 4) & 1
    x5 = (bitInput >> 5) & 1

    bitSet = []

    for i0 in range(x0 + 1):
        for i1 in range(x1 + 1):
            for i2 in range(x2 + 1):
                for i3 in range(x3 + 1):
                    for i4 in range(x4 + 1):
                        for i5 in range(x5 + 1):

                            bitSet_i = i0 ^ (i1 << 1) ^ (i2 << 2) ^ (i3 << 3) ^ (i4 << 4) ^ (i5 << 5)
                            bitSet.append(bitSet_i)

    return bitSet


# SPEEDY Sbox FTDDT compute
# e.g. 0bin0001001 -> 0bin**000*
def ComputeFTDDT_i(input, output):
    outputSet = BitToSet(output)
    outputLen = len(outputSet)

    ans = 0
    for i in range(outputLen):
        ans = ans + DDT[input][outputSet[i]]

    return ans

def ComputeFTDDT():
    FTDDT = []
    for i in range(1 << 6):

        FTDDT.append([])

        for j in range(1 << 6):
            FTDDT[i].append(0)

    FTDDT[0][0] = 64

    for input in range(1, 1 << 6):

        for output in range(1, 1 << 6):
            FTDDT[input][output] = ComputeFTDDT_i(input, output)

    return FTDDT

def Exprement_i(plain):
    p1 = (plain >> (6 * 6)) & 0b111111
    p2 = (plain >> (6 * 5)) & 0b111111
    p3 = (plain >> (6 * 4)) & 0b111111
    p4 = (plain >> (6 * 3)) & 0b111111
    p5 = (plain >> (6 * 2)) & 0b111111
    p6 = (plain >> (6 * 1)) & 0b111111
    p7 = plain & 0b111111

    Xored_p1 = p1 ^ 0b010000
    Xored_p2 = p2 ^ 0b010000
    Xored_p3 = p3 ^ 0b010000
    Xored_p4 = p4 ^ 0b001000
    Xored_p5 = p5 ^ 0b001000
    Xored_p6 = p6 ^ 0b000100
    Xored_p7 = p7 ^ 0b000100

    outD1 = S[p1] ^ S[Xored_p1]
    outD2 = S[p2] ^ S[Xored_p2]
    outD3 = S[p3] ^ S[Xored_p3]
    outD4 = S[p4] ^ S[Xored_p4]
    outD5 = S[p5] ^ S[Xored_p5]
    outD6 = S[p6] ^ S[Xored_p6]
    outD7 = S[p7] ^ S[Xored_p7]

    if ( outD1 & 0b001000) != 0:
        return 0
    if ( outD2 & 0b000011) != 0:
        return 0
    if ( outD3 & 0b100000) != 0:
        return 0
    if ( outD4 & 0b110000) != 0:
        return 0
    if ( outD5 & 0b000011) != 0:
        return 0
    if ( outD6 & 0b000100) != 0:
        return 0
    if ( outD7 & 0b100100) != 0:
        return 0

    return 1

import math
FTDDT = ComputeFTDDT()
p1 = FTDDT[0b010000][0b110111]/64
p2 = FTDDT[0b010000][0b111100]/64
p3 = FTDDT[0b010000][0b011111]/64

p4 = FTDDT[0b001000][0b001111]/64
p5 = FTDDT[0b001000][0b111100]/64

p6 = FTDDT[0b000100][0b111011]/64
p7 = FTDDT[0b000100][0b011011]/64

# print(math.log(p1,2))
# print(math.log(p2,2))
# print(math.log(p3,2))
# print(math.log(p4,2))
# print(math.log(p5,2))
# print(math.log(p6,2))
# print(math.log(p7,2))
p = p1 * p2 * p3 * p4 * p5 * p6 * p7
print("probability calculated from FTDDT: 2^{",math.log(p,2), "}",sep = "")

import random
ans = 0
for i in range(1 << 20):
    plain = random.randint(0, 1 << 42)
    ans = ans + Exprement_i(plain)
print("probability calculated from exprement:{", math.log(ans/(1 << 20),2),"}",sep = "")































