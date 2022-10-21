from SboxTool import  SboxTool

S = [ 0x08,0x00,0x09,0x03,0x38,0x10,0x29,0x13,0x0c,0x0d,0x04,0x07,0x30,0x01,0x20,0x23,
                        0x1a,0x12,0x18,0x32,0x3e,0x16,0x2c,0x36,0x1c,0x1d,0x14,0x37,0x34,0x05,0x24,0x27,
                        0x02,0x06,0x0b,0x0f,0x33,0x17,0x21,0x15,0x0a,0x1b,0x0e,0x1f,0x31,0x11,0x25,0x35,
                        0x22,0x26,0x2a,0x2e,0x3a,0x1e,0x28,0x3c,0x2b,0x3b,0x2f,0x3f,0x39,0x19,0x2d,0x3d ]

DifferentialM = [0, 1, 5, 9, 15, 21, 26]

Speedy_Sbox = SboxTool(S, 6)

Speedy_Sbox.DDTcompute()

DDT = Speedy_Sbox.DDT

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

    sys.stdout = old  # 还原系统输出
    file.close()

# Assert cvc variable
def SName(VarTag ,round, tag, i):

    command = VarTag + "_" + str(round) + "_" + str(tag) + "_" + str(i)

    return command

# Command => Assert(Command);
def AssertCommand(input):
    command = "ASSERT(" + input + ");"

    return command


# return Assert( VarName_round_tag_loc);
def AssertVariableCommand(VarName ,round, tag, loc):

    command = SName(VarName, round, tag, loc)

    return command

# print Asserted command to fileName
def AssertPrint(fileName, command):
    import sys
    file = open(fileName, 'a')
    old = sys.stdout
    sys.stdout = file

    print(command)

    sys.stdout = old  # 还原系统输出
    file.close()

# Assert a round Variable
def AssertVariable(fileName, VarName ,round, tag, locNum, VarLong):

    command = ""

    for loc in range(locNum - 1):

        command = command + AssertVariableCommand(VarName, round, tag, str(loc)) + ",  "

    command = command + AssertVariableCommand(VarName, round, tag, str(locNum - 1)) + ": BITVECTOR(" + str(VarLong) +");"

    AssertPrint(fileName, command)

    AssertPrint(fileName,"  ")

# return i-th Sbox
def SboxName(VarTag ,round, tag, SboxTag):

    command = ""

    for i in range(5):

        command = command + VarTag + "_" + str(round) + "_" + str(tag) + "_" + str(i) + "[" + str(SboxTag) + ":" + str(SboxTag) + "]@"

    command = command + VarTag + "_" + str(round) + "_" + str(tag) + "_" + str(5) + "[" + str(SboxTag) + ":" + str(SboxTag) + "]"

    return command

def ShiftX(VarTag, round, tag, SboxTag, X):

    X = X % 32

    if X == 0:
        command = SName(VarTag, round, tag, SboxTag)

    else:

        command = "((( " + VarTag + "_" + str(round) + "_" + str(tag) + "_" + str(SboxTag)+" << " + str (X) + ")[31 :0]) | (( " + VarTag+ "_" + str(round) + "_" + str(tag) + "_" + str(SboxTag)+" >> " + str(32 - X) + ")[31:0]))"

    return command

def DDTCVCprint(fileName, DDT):
    import sys
    import math

    file = open(fileName, 'a')
    old = sys.stdout
    sys.stdout = file

    print("DDT: ARRAY BITVECTOR(12) OF BITVECTOR(15);", sep="")

    for input in range(1 << 6):

        for output in range(1 << 6):

            inprint = bin(input)[2:].rjust(6, '0')
            outprint = bin(output)[2:].rjust(6, '0')

            # Cal DDT p in 0bin....
            p = DDT[input][output]

            if p == 0:

                plog = ( 1 << 15) - 1

            else:

                plog = math.ceil(-1000 * math.log( p / (1 << 6), 2))


            pprint = bin(plog)[2:].rjust(15, '0')

            print("ASSERT(DDT[0bin", inprint, outprint, "] = 0bin", pprint, ");", sep="")

    sys.stdout = old  # 还原系统输出
    file.close()

#
# # The DDT output which forward propagate truncte is called FTDDT
# # compute FTDDT
# def BinToArray(input):
#
#     Array = []
#
#     State = input
#
#     for i in range(6):
#
#         Array.append(State % 2)
#
#         State = int(State / 2)
#
#     return Array
#
#
# def ArrayToBin(Array):
#
#     command = "0bin"
#
#     for i in range(6):
#
#         command = command + str(Array[5 - i])
#
#     return command
#
# # input is tuncated
# def CalFTDDT_i(input, output, DDT):
#
#     # Convert input from integer to array
#     inputArray = BinToArray(input)
#
#     p = 0
#
#     for i5 in range(inputArray[5] + 1):
#         for i4 in range(inputArray[4] + 1):
#             for i3 in range(inputArray[3] + 1):
#                 for i2 in range(inputArray[2] + 1):
#                     for i1 in range(inputArray[1] + 1):
#                         for i0 in range(inputArray[0] + 1):
#
#                             inputi = (i5 << 5) ^ (i4 << 4) ^ (i3 << 3) ^ (i2 << 2) ^ (i1 << 1) ^ (i0 << 0)
#
#                             p = DDT[inputi][output] + p
#
#
#     return p
#
# def CalFTDDT(DDT):
#
#     FTDDT = []
#
#     for i in range(1 << 6):
#
#         FTDDT.append([])
#
#         for j in range(1 << 6):
#
#             FTDDT[i].append(0)
#
#
#     for input in range(1 << 6):
#
#         for output in range(1 << 6):
#
#             FTDDT[input][output] = CalFTDDT_i(input, output, DDT)
#
#     return FTDDT
#
# FTDDT = CalFTDDT(DDT)
#
# # print FTDDT to cvc file
# def FTDDTprint(fileName, FTDDT):
#     import sys
#     import math
#
#     file = open(fileName, 'a')
#     old = sys.stdout
#     sys.stdout = file
#
#     print("FTDDT: ARRAY BITVECTOR(12) OF BITVECTOR(15);", sep="")
#
#     for input in range(1 << 6):
#
#         for output in range(1 << 6):
#
#             inprint = bin(input)[2:].rjust(6, '0')
#             outprint = bin(output)[2:].rjust(6, '0')
#
#             # Cal DDT p in 0bin....
#             p = FTDDT[input][output]
#
#             if p == 0:
#
#                 plog = ( 1 << 15) - 1
#
#             else:
#
#                 plog = math.ceil(-1000 * math.log( p / (1 << 6), 2))
#
#
#             pprint = bin(plog)[2:].rjust(15, '0')
#
#             print("ASSERT(FTDDT[0bin", inprint, outprint, "] = 0bin", pprint, ");", sep="")
#
#     sys.stdout = old  # 还原系统输出
#     file.close()

def SboxCVCPrint_NotCommand_i( TableTag,VarName, round, tag, SboxTag):

    command = "NOT( " + TableTag + "[" + SboxName(VarName, round, tag, SboxTag) + "@" + SboxName(VarName, round, tag + 1, SboxTag) + "] = 0bin111111111111111 )"

    return command

def SboxCVCPrint_P_Command_i(TableTag, VarName, round, tag, SboxTag, PName, PTag):

    command = "IF " + SboxName(VarName, round, tag, SboxTag) + " = 0bin000000 THEN " + SName(PName, round, PTag, SboxTag) + " = 0bin"

    for i in range(15):

        command = command + "0"

    command = command + " ELSE " + SName(PName, round, PTag, SboxTag) + " = " + TableTag + "[" + SboxName(VarName, round, tag, SboxTag) + "@" + SboxName(VarName, round, tag + 1, SboxTag) + "] ENDIF "

    return command

def SboxCVCPrint_P_Print(fileName, TableTag, VarName, round, tag, SboxNum, PName, PTag):

    for SboxTag in range(SboxNum):

        NotCommand = SboxCVCPrint_NotCommand_i(TableTag, VarName, round, tag, SboxTag)
        NotCommand = AssertCommand(NotCommand)
        AssertPrint(fileName, NotCommand)
        AssertPrint(fileName, "  ")

        command = SboxCVCPrint_P_Command_i(TableTag, VarName, round, tag, SboxTag, PName, PTag)
        command = AssertCommand(command)
        AssertPrint(fileName, command)
        AssertPrint(fileName, "  ")

def SCCVCPrint_i(VarTag, round, tag, i):

    if i == 0:

        command = "ASSERT( " + SName(VarTag, round, tag + 1, i) + " = " + SName(VarTag, round, tag, i) + ");"

    else:

        command = "ASSERT( " + SName(VarTag, round, tag + 1, i) + " = " + ShiftX(VarTag, round, tag, i,
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

    sys.stdout = old  # 还原系统输出
    file.close()

def Differential_MCCVCPrint_i(VarTag, round, tag, i, DifferentialM):

    command = "ASSERT( " + SName(VarTag, round + 1, 0, i) + " = "

    for j in range(7):

        command = command + "BVXOR( " + ShiftX(VarTag, round, tag, i, ( 32 - DifferentialM[j])) + ","

    command = command + "0b"

    for i in range(32):

        command = command + "0"

    for j in range(7):

        command = command + ")"

    command = command + ");"

    return command

def Differential_MCCVCPrint( fileName, VarTag, round, tag,DifferentialM):
    import sys
    file = open(fileName, 'a')
    old = sys.stdout
    sys.stdout = file

    for i in range(6):

        print(Differential_MCCVCPrint_i(VarTag, round, tag, i, DifferentialM))

    sys.stdout = old
    file.close()

# For the probabilty p need to mul 1000, too
def Assert_BVLE(fileName, inputP):

    p = hex(inputP * 1000)[2:].rjust( int(24/4), "0")

    command = "ASSERT(BVLE(P, 0hex" + p + " ));"

    AssertPrint(fileName, command)

def EndPrint(fileName):
    import sys
    file = open(fileName, 'a')
    old = sys.stdout
    sys.stdout = file

    print("QUERY(FALSE);")
    print("COUNTEREXAMPLE;")

    sys.stdout = old  # 还原系统输出
    file.close()

def AssertP_Begin(fileName):

    AssertPrint(fileName, "P:BITVECTOR(24);")

def AssertP_End(fileName):

    command = "P =  BVPLUS(24,"

    for SboxTag in range(32):

        command = command + "0bin000000000@" + SName("P", 1, 1, SboxTag) + ","

    for SboxTag in range(32):
        command = command + "0bin000000000@" + SName("P", 2, 0, SboxTag) + ","

    for SboxTag in range(32):
        command = command + "0bin000000000@" + SName("P", 2, 1, SboxTag) + ","

    for SboxTag in range(32):
        command = command + "0bin000000000@" + SName("P", 3, 0, SboxTag) + ","

    for SboxTag in range(32):
        command = command + "0bin000000000@" + SName("P", 3, 1, SboxTag) + ","

    command = command + "0bin000000000000000000000000)"

    command = AssertCommand(command)

    AssertPrint(fileName, command)


# def AssertSboxNum_End(fileName):
#     command = "SboxNum =  BVPLUS(8,"
#
#     # p_0_0, Differential
#     for SboxTag in range(32):
#         command = command + SName("SboxNum", 0, 1, SboxTag) + ","
#
#     for SboxTag in range(32):
#         command = command + SName("SboxNum", 2, 2, SboxTag) + ","
#
#
#
#
#     command = command + "0bin00000000)"
#
#     command = AssertCommand(command)
#
#     AssertPrint(fileName, command)

def AssertActSboxP(fileName, VarName, round, Tag, PName, PTag):

    for i in range(32):
        command = "IF " + SboxName(VarName, round, Tag, i) + " = 0bin000000 THEN " + SName(PName, round, PTag,
                                                                                          i) + " = 0bin"
        
        for j in range(15):

            command = command + "0"

        command = command + " ELSE " + SName(PName, round, PTag, i) + " = 0bin"

        ActSboxP = 6 * 1000
        ActSboxP_str = bin(ActSboxP)[2:].rjust(15, "0")
        command = command + ActSboxP_str + " ENDIF"

        command = AssertCommand(command)
        AssertPrint(fileName, command)

def SetSboxValue_i(fileName, VarName, round, Tag, SboxLoc, Value):

    command = SboxName(VarName, round, Tag, SboxLoc) + " = " + Value
    command = AssertCommand(command)
    AssertPrint(fileName, command)

def SetSboxValue(fileName, VarName, round, Tag, ActSboxLoc, Value):

    for i in range(32):

        if i in ActSboxLoc:

            SetSboxValue_i(fileName, VarName, round, Tag, i, Value)

        else:

            SetSboxValue_i(fileName, VarName, round, Tag, i, "0b000000")


# def AssertSboxNum_Begin(fileName):
#
#     AssertPrint(fileName, "SboxNum:BITVECTOR(8);")
#
#
# def Assert_SboxNum_BVLE(fileName):
#
#
#     command = "ASSERT(BVLE(SboxNum, 0hex20));"
#
#     AssertPrint(fileName, command)









def main(fileName, p, ActLocArray, ActValue):

    ClearFile(fileName)

    AssertVariable(fileName, "S", 1, 3, 6, 32)
    AssertVariable(fileName, "S", 1, 4, 6, 32)

    AssertVariable(fileName, "S", 2, 0, 6, 32)
    AssertVariable(fileName, "S", 2, 1, 6, 32)
    AssertVariable(fileName, "S", 2, 2, 6, 32)
    AssertVariable(fileName, "S", 2, 3, 6, 32)
    AssertVariable(fileName, "S", 2, 4, 6, 32)

    AssertVariable(fileName, "S", 3, 0, 6, 32)
    AssertVariable(fileName, "S", 3, 1, 6, 32)
    AssertVariable(fileName, "S", 3, 2, 6, 32)
    AssertVariable(fileName, "S", 3, 3, 6, 32)
    AssertVariable(fileName, "S", 3, 4, 6, 32)


    AssertVariable(fileName, "P", 1, 1, 32, 15)

    AssertVariable(fileName, "P", 2, 0, 32, 15)
    AssertVariable(fileName, "P", 2, 1, 32, 15)

    AssertVariable(fileName, "P", 3, 0, 32, 15)
    AssertVariable(fileName, "P", 3, 1, 32, 15)


    AssertP_Begin(fileName)

    DDTCVCprint(fileName, DDT)

    SCCVCPrint(fileName, "S", 1, 3)
    Differential_MCCVCPrint(fileName, "S", 1, 4, DifferentialM)

    SboxCVCPrint_P_Print(fileName, "DDT", "S", 2, 0, 32, "P", 0)
    SCCVCPrint(fileName, "S", 2, 1)
    SboxCVCPrint_P_Print(fileName, "DDT", "S", 2, 2, 32, "P", 1)
    SCCVCPrint(fileName, "S", 2, 3)
    Differential_MCCVCPrint(fileName, "S", 2, 4, DifferentialM)

    SboxCVCPrint_P_Print(fileName, "DDT", "S", 3, 0, 32, "P", 0)
    SCCVCPrint(fileName, "S", 3, 1)
    SboxCVCPrint_P_Print(fileName, "DDT", "S", 3, 2, 32, "P", 1)
    SCCVCPrint(fileName, "S", 3, 3)

    SetSboxValue(fileName, "S", 3, 4, ActLocArray, ActValue)

    AssertActSboxP(fileName, "S", 1, 3, "P", 1)

    AssertP_End(fileName)

    Assert_BVLE(fileName, p)

    EndPrint(fileName)

#
# def makeValue(actLoc):
#
#     Value = 1 << actLoc
#
#     command = "0b" + bin(Value)[2:].rjust(6,"0")
#
#     return command


# ActValue = makeValue(4)
fileName = "SPEEDY_Differential_FirstTrail.cvc"
p = 100
ActLoc = [0]
ActValue = "0b000010"
main(fileName, p, ActLoc, ActValue)











