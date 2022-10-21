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
