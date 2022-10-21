class SboxTool :
    def __init__(self, Sbox, SboxSize):
        self.Sbox = Sbox
        self.SboxSize = SboxSize
        self.number = (1 << SboxSize)

    def DDTcompute(self):

        DDT = [[0]*self.number for i in range(self.number)]

        for plaintextA in range(self.number):
            for inXor in range(self.number):
                plaintextB = plaintextA ^ inXor
                cipherA = self.Sbox[plaintextA]
                cipherB = self.Sbox[plaintextB]
                outXor = cipherA ^ cipherB
                DDT[inXor][outXor] = DDT[inXor][outXor] + 1

        self.DDT = DDT

    def LATcompute(self):

        LAT = [[0] * self.number for i in range(self.number)]

        for inmask in range(self.number):
            for outmask in range(self.number):
                for intext in range(self.number):
                    outtext = self.Sbox[intext]
                    outand = outtext & outmask
                    inand = intext & inmask
                    andresult = outand ^ inand
                    andbit = bin(andresult)[2:]
                    answer = 0

                    for i in range(len(andbit)):
                        answer = answer ^ int(andbit[i])

                    if answer == 0:
                        LAT[inmask][outmask] = LAT[inmask][outmask] + 1

        for i in range(self.number):
            for j in range(self.number):
                LAT[i][j] = int(abs(LAT[i][j] - self.number / 2))

        self.LAT = LAT