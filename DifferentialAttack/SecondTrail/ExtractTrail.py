from SboxTool import SboxTool
import numpy as np

S = [0x08,0x00,0x09,0x03,0x38,0x10,0x29,0x13,0x0c,0x0d,0x04,0x07,0x30,0x01,0x20,0x23,
                        0x1a,0x12,0x18,0x32,0x3e,0x16,0x2c,0x36,0x1c,0x1d,0x14,0x37,0x34,0x05,0x24,0x27,
                        0x02,0x06,0x0b,0x0f,0x33,0x17,0x21,0x15,0x0a,0x1b,0x0e,0x1f,0x31,0x11,0x25,0x35,
                        0x22,0x26,0x2a,0x2e,0x3a,0x1e,0x28,0x3c,0x2b,0x3b,0x2f,0x3f,0x39,0x19,0x2d,0x3d ]


Speedy_Sbox = SboxTool(S, 6)

Speedy_Sbox.DDTcompute()

def BinToInt(input):

    res = 0

    for i in range(6):

        x = 5 - i
        res = res + ( int(input[x]) << i)

    return res

def HexToInt(input):
    if input == "0":
        return int(0)
    if input == "1":
        return int(1)
    if input == "2":
        return int(2)
    if input == "3":
        return int(3)
    if input == "4":
        return int(4)
    if input == "5":
        return int(5)
    if input == "6":
        return int(6)
    if input == "7":
        return int(7)
    if input == "8":
        return int(8)
    if input == "9":
        return int(9)
    if input == "A":
        return int(10)
    if input == "B":
        return int(11)
    if input == "C":
        return int(12)
    if input == "D":
        return int(13)
    if input == "E":
        return int(14)
    if input == "F":
        return int(15)

def SToInt(input):

    output = 0

    for i in range(8):
        x = 7 - i
        outputi = HexToInt(input[x])
        output = output + ( outputi << ( 4 * i))

    return output




def GenerateP(input, output, DDT):

    return DDT[BinToInt(input)][BinToInt(output)]

def SName(round, tag, Column):

    command = "S_" + str(round) + "_" + str(tag) + "_" + str(Column) + " "

    return command

def GetColumn(infileName, round, tag, Column):

    SearchSbox = SName(round, tag, Column)

    file = open(infileName, 'r')

    line = file.readline()

    while(line):

        compare = line[8:16]

        if compare == SearchSbox:
            file.close()
            return line[20:28]

        line = file.readline()


def GetSboxValue_i(input, SboxLoc):

    res = ( input >> SboxLoc) & 1

    return str(res)


def GetSboxValue(infileName, round, tag, SboxLoc):

    res = ""

    for i in range(6):

        Columni = GetColumn(infileName, round, tag, i)
        IntColumni = SToInt(Columni)
        resi = GetSboxValue_i(IntColumni, SboxLoc)

        res = res + resi

    return res

def PrintToFile(fileName, command):
    import sys
    file = open(fileName, 'a')
    old = sys.stdout
    sys.stdout = file

    print(command, end = "", sep = "")

    sys.stdout = old
    file.close()

def PrintToFile_clear(fileName):
    import sys
    file = open(fileName, 'w')
    old = sys.stdout
    sys.stdout = file



    sys.stdout = old
    file.close()

def PrintToFile_NextRow(fileName):
    import sys
    file = open(fileName, 'a')
    old = sys.stdout
    sys.stdout = file

    print()

    sys.stdout = old
    file.close()

def CalP(P):

    if P == 2:
        return [1, 5]

    if P == 4:
        return [1, 4]

    if P == 6:
        return [3, 5]

    if P == 8:
        return [1, 3]

def CalAllP(AllP, P):

    AllP[0] = AllP[0] * P[0]
    AllP[1] = AllP[1] + P[1]


def Pprint(fileName, tag, DDT, input, output, AllP):

    inputint = BinToInt(input)
    outputint = BinToInt(output)

    command = "    "
    if ( (tag == 0) | (tag == 2)):
        if inputint == 0:
            command = command + "  "
        else:
            P = DDT[inputint][outputint]
            Padd = CalP(P)
            CalAllP(AllP, Padd)

            command = command + str(P)

    else:
        command = command + "  "

    command = command + "    "

    PrintToFile(fileName, command)


def LuXianTiQu_i(infileName, outfileName, StartRound, StartTag, EndRound, EndTag, SboxLoc, AllP):

    for i in range(StartTag, 5):

        commond = GetSboxValue(infileName, StartRound, i, SboxLoc)
        PrintToFile(outfileName, commond)

        if (i == 4):

            PrintToFile(outfileName, "         ")

        else:

            input = GetSboxValue(infileName, StartRound, i, SboxLoc)
            output = GetSboxValue(infileName, StartRound, i + 1, SboxLoc)

            Pprint(outfileName, i, Speedy_Sbox.DDT, input, output, AllP)

    for roundi in range(StartRound + 1, EndRound):

        for i in range(5):
            commond = GetSboxValue(infileName, roundi, i, SboxLoc)
            PrintToFile(outfileName, commond)

            if (i == 4):

                PrintToFile(outfileName, "            ")

            else:

                input = GetSboxValue(infileName, roundi, i, SboxLoc)
                output = GetSboxValue(infileName, roundi, i + 1, SboxLoc)

                Pprint(outfileName, i, Speedy_Sbox.DDT, input, output, AllP)

    for i in range(EndTag):

        commond = GetSboxValue(infileName, EndRound, i, SboxLoc)
        PrintToFile(outfileName, commond)

        input = GetSboxValue(infileName, EndRound, i, SboxLoc)
        output = GetSboxValue(infileName, EndRound, i + 1, SboxLoc)

        Pprint(outfileName, i, Speedy_Sbox.DDT, input, output, AllP)

    commond = GetSboxValue(infileName, EndRound, EndTag, SboxLoc)
    PrintToFile(outfileName, commond)

    PrintToFile_NextRow(outfileName)



def ExtractTrail(infileName, outfileName, StartRound, StartTag, EndRound, EndTag):
    AllP = [1, 0]

    PrintToFile_clear(outfileName)

    for SboxLoc in range(32):
        LuXianTiQu_i(infileName, outfileName, StartRound, StartTag, EndRound, EndTag, SboxLoc, AllP)

    PrintToFile_NextRow(outfileName)
    PrintToFile_NextRow(outfileName)
    PrintToFile(outfileName, "P：")
    PrintToFile(outfileName, AllP)

    import math
    p =  math.log(AllP[0] ,2)
    pIndex = p - AllP[1]
    pStr = "2^{" + str(pIndex) + "}"

    PrintToFile(outfileName, "            ")
    PrintToFile(outfileName, pStr)

    print(infileName, "P：", AllP, "    ",pStr)

infileName = "SPEEDY_Differential_SecondTrail.txt"
outfileName = "out_SPEEDY_Differential_SecondTrail.txt"
StartRound = 3
StartTag = 4
EndRound = 6
EndTag = 0

ExtractTrail(infileName, outfileName, StartRound, StartTag, EndRound, EndTag)




print(0x0221E0)



