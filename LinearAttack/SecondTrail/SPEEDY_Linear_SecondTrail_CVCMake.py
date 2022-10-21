from SboxTool import  SboxTool

S = [ 0x08,0x00,0x09,0x03,0x38,0x10,0x29,0x13,0x0c,0x0d,0x04,0x07,0x30,0x01,0x20,0x23,
                        0x1a,0x12,0x18,0x32,0x3e,0x16,0x2c,0x36,0x1c,0x1d,0x14,0x37,0x34,0x05,0x24,0x27,
                        0x02,0x06,0x0b,0x0f,0x33,0x17,0x21,0x15,0x0a,0x1b,0x0e,0x1f,0x31,0x11,0x25,0x35,
                        0x22,0x26,0x2a,0x2e,0x3a,0x1e,0x28,0x3c,0x2b,0x3b,0x2f,0x3f,0x39,0x19,0x2d,0x3d ]

M = [0, 6, 11, 17, 23, 27, 31]

Speedy_Sbox = SboxTool(S, 6)

Speedy_Sbox.LATcompute()

LAT = Speedy_Sbox.LAT

tagNum = 5
VecNum = 32
VecLong = 6
SboxNum = 32
PNum = 2

def ClearFile(fileName):
    import sys
    file = open(fileName, 'w')
    old = sys.stdout
    sys.stdout = file

    print("", end = "",sep = "")

    sys.stdout = old
    file.close()

def SName(VarTag ,round, tag, i):

    command = VarTag + "_" + str(round) + "_" + str(tag) + "_" + str(i)

    return command

def AssertCommand(input):
    command = "ASSERT(" + input + ");"

    return command

def AssertVariableCommand(VarName ,round, tag, loc):

    command = SName(VarName, round, tag, loc)

    return command

def AssertPrint(fileName, command):
    import sys
    file = open(fileName, 'a')
    old = sys.stdout
    sys.stdout = file

    print(command)

    sys.stdout = old
    file.close()

def AssertVariable(fileName, VarName ,round, tag, locNum, VarLong):

    command = ""

    for loc in range(locNum - 1):

        command = command + AssertVariableCommand(VarName, round, tag, str(loc)) + ",  "

    command = command + AssertVariableCommand(VarName, round, tag, str(locNum - 1)) + ": BITVECTOR(" + str(VarLong) +");"

    AssertPrint(fileName, command)

    AssertPrint(fileName,"  ")

def SboxName(VarTag ,round, tag, SboxTag):

    command = ""

    for i in range(5):

        command = command + VarTag + "_" + str(round) + "_" + str(tag) + "_" + str(i) + "[" + str(SboxTag) + ":" + str(SboxTag) + "]@"

    command = command + VarTag + "_" + str(round) + "_" + str(tag) + "_" + str(5) + "[" + str(SboxTag) + ":" + str(SboxTag) + "]"

    return command

def ShifX(VarTag, round, tag, SboxTag, X):

    X = X % 32

    if X == 0:
        command = SName(VarTag, round, tag, SboxTag)

    else:

        command = "((( " + VarTag + "_" + str(round) + "_" + str(tag) + "_" + str(SboxTag)+" << " + str (X) + ")[31 :0]) | (( " + VarTag+ "_" + str(round) + "_" + str(tag) + "_" + str(SboxTag)+" >> " + str(32 - X) + ")[31:0]))"

    return command

def LATCVCprint(fileName, LAT):
    import sys
    import math

    file = open(fileName, 'a')
    old = sys.stdout
    sys.stdout = file

    print("LAT: ARRAY BITVECTOR(12) OF BITVECTOR(12);", sep="")

    for input in range(1 << 6):

        for output in range(1 << 6):

            inprint = bin(input)[2:].rjust(6, '0')
            outprint = bin(output)[2:].rjust(6, '0')

            # Cal LAT cor in 0bin....
            cor = 2 * LAT[input][output]

            if cor == 0:

                corlog = ( 1 << 12) - 1

            elif cor == 1 << 6:

                corlog = 0

            else:

                corlog = math.ceil(-1000 * math.log( cor / (1 << 6), 2))


            corprint = bin(corlog)[2:].rjust(12, '0')

            print("ASSERT(LAT[0bin", inprint, outprint, "] = 0bin", corprint, ");", sep="")

    sys.stdout = old
    file.close()

def SboxCVCPrint_LAT_NotCommand_i(VarName, round, tag, SboxTag):

    command = "NOT( " + "LAT[" + SboxName(VarName, round, tag, SboxTag) + "@" + SboxName(VarName, round, tag + 1, SboxTag) + "] = 0bin111111111111 )"

    return command

def SboxCVCPrint_LAT_P_Command_i(VarName, round, tag, SboxTag, PName, PTag):

    command = "IF " + SboxName(VarName, round, tag, SboxTag) + " = 0bin000000 THEN " + SName(PName, round, PTag, SboxTag) + " = 0bin"

    for i in range(12):

        command = command + "0"

    command = command + " ELSE " + SName(PName, round, PTag, SboxTag) + " = LAT[" + SboxName(VarName, round, tag, SboxTag) + "@" + SboxName(VarName, round, tag + 1, SboxTag) + "] ENDIF "

    return command

def SboxCVCPrint_LAT_P_Print(fileName, VarName, round, tag, SboxNum, PName, PTag):

    for SboxTag in range(SboxNum):

        NotCommand = SboxCVCPrint_LAT_NotCommand_i(VarName, round, tag, SboxTag)
        NotCommand = AssertCommand(NotCommand)
        AssertPrint(fileName, NotCommand)
        AssertPrint(fileName, "  ")

        command = SboxCVCPrint_LAT_P_Command_i(VarName, round, tag, SboxTag, PName, PTag)
        command = AssertCommand(command)
        AssertPrint(fileName, command)
        AssertPrint(fileName, "  ")

def SCCVCPrint_i(VarTag, round, tag, i):

    if i == 0:

        command = "ASSERT( " + SName(VarTag, round, tag + 1, i) + " = " + SName(VarTag, round, tag, i) + ");"

    else:

        command = "ASSERT( " + SName(VarTag, round, tag + 1, i) + " = " + ShifX(VarTag, round, tag, i,
                                                                                       (32 - i) % 32) + ");"

    return command

def SCCVCPrint(fileName, VarTag, round, tag):
    import sys
    file = open(fileName, 'a')
    old = sys.stdout
    sys.stdout = file

    print(SCCVCPrint_i(VarTag, round, tag, 0))
    print(SCCVCPrint_i(VarTag, round, tag, 1))
    print(SCCVCPrint_i(VarTag, round, tag, 2))
    print(SCCVCPrint_i(VarTag, round, tag, 3))
    print(SCCVCPrint_i(VarTag, round, tag, 4))
    print(SCCVCPrint_i(VarTag, round, tag, 5))
    print()

    sys.stdout = old
    file.close()

def MCCVCPrint_i(VarTag, round, tag, i, M):

    command = "ASSERT( " + SName(VarTag, round, tag, i) + " = "

    for j in range(7):

        command = command + "BVXOR( " + ShifX(VarTag, round + 1, 0, i, ( 32 - M[j])) + ","

    command = command + "0b"

    for i in range(32):

        command = command + "0"

    for j in range(7):

        command = command + ")"

    command = command + ");"

    return command

def MCCVCPrint( fileName, VarTag, round, tag, M):
    import sys
    file = open(fileName, 'a')
    old = sys.stdout
    sys.stdout = file

    for i in range(6):

        print(MCCVCPrint_i(VarTag, round, tag, i, M))

    sys.stdout = old
    file.close()

def Assert_BVLE(fileName, inputP):

    p = hex(inputP * 1000)[2:].rjust( int(24 / 4), "0")

    command = "ASSERT(BVLE(P, 0hex" + p + " ));"

    AssertPrint(fileName, command)

def EndPrint(fileName):
    import sys
    file = open(fileName, 'a')
    old = sys.stdout
    sys.stdout = file

    print("QUERY(FALSE);")
    print("COUNTEREXAMPLE;")

    sys.stdout = old
    file.close()

def AssertP_Begin(fileName):
    AssertPrint(fileName, "P:BITVECTOR(24);")

def AssertP_END(fileName):

    command = "P =  BVPLUS(24,"

    for SboxTag in range(32):
        command = command + "  0bin000000000000@" + SName("P", 3, 0, SboxTag) + ","

    for SboxTag in range(32):
        command = command + "  0bin000000000000@" + SName("P", 3, 1, SboxTag) + ","

    for SboxTag in range(32):
        command = command + "  0bin000000000000@" + SName("P", 4, 0, SboxTag) + ","

    for SboxTag in range(32):
        command = command + "  0bin000000000000@" + SName("P", 4, 1, SboxTag) + ","

    for SboxTag in range(32):
        command = command + "  0bin000000000000@" + SName("P", 5, 0, SboxTag) + ","




    command = command + "0bin000000000000000000000000)"

    command = AssertCommand(command)

    AssertPrint(fileName, command)

# Assert S_0_3 active SboxNum
def AssertActRowP(fileName, VarName, round, Tag, PName, PTag):

    for i in range(32):

        command = "IF " + SboxName(VarName, round, Tag, i) + " = 0bin000000 THEN " + SName(PName, round, PTag, i ) + " = 0bin"

        for j in range(12):

            command = command + "0"

        command = command + " ELSE " + SName(PName, round, PTag, i )  + " = 0bin011111010000 ENDIF"

        command = AssertCommand(command)
        AssertPrint(fileName, command)

def AssertZeroSbox(fileName, round, tag, SboxLoc):

    command = SboxName("S", round, tag, SboxLoc) + "= 0bin000000"

    command = AssertCommand(command)

    AssertPrint(fileName, command)

def AssertNotZeroSbox(fileName, round, tag, SboxLoc, SboxValue):

    command = SboxName("S", round, tag, SboxLoc) + "= " + SboxValue

    command = AssertCommand(command)

    AssertPrint(fileName, command)

def AssertSboxNotAllZero(fileName, round, Tag, SboxLoc, SboxValue):

    for i in range(SboxNum):

        if i in SboxLoc:

            AssertNotZeroSbox(fileName, round, Tag, i, SboxValue)

        else:

            AssertZeroSbox(fileName, round, Tag, i)


def main(fileName, p, SboxLoc, SboxValue):

    ClearFile(fileName)

    M = [0, 6, 11, 17, 23, 27, 31]

    AssertVariable(fileName, "S", 3, 0, 6, 32)
    AssertVariable(fileName, "S", 3, 1, 6, 32)
    AssertVariable(fileName, "S", 3, 2, 6, 32)
    AssertVariable(fileName, "S", 3, 3, 6, 32)
    AssertVariable(fileName, "S", 3, 4, 6, 32)

    AssertVariable(fileName, "S", 4, 0, 6, 32)
    AssertVariable(fileName, "S", 4, 1, 6, 32)
    AssertVariable(fileName, "S", 4, 2, 6, 32)
    AssertVariable(fileName, "S", 4, 3, 6, 32)
    AssertVariable(fileName, "S", 4, 4, 6, 32)

    AssertVariable(fileName, "S", 5, 0, 6, 32)


    AssertVariable(fileName, "P", 3, 0, 32, 12)
    AssertVariable(fileName, "P", 3, 1, 32, 12)

    AssertVariable(fileName, "P", 4, 0, 32, 12)
    AssertVariable(fileName, "P", 4, 1, 32, 12)

    AssertVariable(fileName, "P", 5, 0, 32, 12)




    AssertP_Begin(fileName)


    LATCVCprint(fileName, LAT)


    SboxCVCPrint_LAT_P_Print(fileName, "S", 3, 0, 32, "P", 0)
    SCCVCPrint(fileName, "S", 3, 1)
    SboxCVCPrint_LAT_P_Print(fileName, "S", 3, 2, 32, "P", 1)
    SCCVCPrint(fileName, "S", 3, 3)
    MCCVCPrint(fileName, "S", 3, 4, M)

    SboxCVCPrint_LAT_P_Print(fileName, "S", 4, 0, 32, "P", 0)
    SCCVCPrint(fileName, "S", 4, 1)
    SboxCVCPrint_LAT_P_Print(fileName, "S", 4, 2, 32, "P", 1)
    SCCVCPrint(fileName, "S", 4, 3)
    MCCVCPrint(fileName, "S", 4, 4, M)

    AssertActRowP(fileName, "S", 5, 0, "P", 0)

    AssertSboxNotAllZero(fileName, 3, 0, SboxLoc, SboxValue)

    AssertP_END(fileName)

    Assert_BVLE(fileName, p)

    EndPrint(fileName)


fileName = "SPEEDY_Linear_SecondTrail.cvc"
p = 50
SboxLoc = [0, 11]
SboxValue = "0bin000010"
main(fileName, p, SboxLoc, SboxValue)