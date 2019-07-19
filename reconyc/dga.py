"""
    UNPREDICTABLE DGA OF RECONYC

    from sample: d7e3bbdc38aa18b214fed3518798b86b
    unpacks to:  db0820a974dbea22d981bd39ddb19518
"""


import random

class Mersenne:

    def __init__(self, seed):
        self.n = 624
        self.w = 32
        self.wm = (2**32) - 1
        self.r = 31
        self.f = 1812433253
        self.a = 0x9908B0DF
        self.u = 11
        self.s = 7
        self.t = 15
        self.d = 0xFFFFFFFF
        self.b = 0x9D2C5680
        self.c = 0xEFC60000
        self.l = 18
        self.m = 397
        self.seed = seed
        self.seed_b = ~seed
        self.mt = self.n*[0]
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = (1 << self.r)

    def seed_mt(self):
        self.mt[0] = self.seed
        for i in range(self.n-1):
            self.mt[i+1] = (self.f * ((self.mt[i] >> 30) ^ self.mt[i]) + i+1) & self.wm


    def extract_number(self):
        if self.seed != self.seed_b:
            self.index = self.n + 1
        if self.index >= self.n:
            if self.index == self.n + 1:
                self.seed_mt()
                self.seed = ~self.seed
                self.seed_b = self.seed
            self.twist()
            self.index = 0

        y = self.mt[self.index]
        y ^= (y >> self.u) & self.d
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= (y >> self.l)
        self.index += 1
        return y

    def twist(self):
        for i in range(self.n-1):
            a = (self.mt[i] & self.upper_mask)
            b = (self.mt[(i+1) % self.n]) & self.lower_mask
            x = a + b
            x = x & self.wm
            xA = (x >> 1)
            if x % 2:
                xA = (xA ^ self.a)
            self.mt[i] = self.mt[(i+self.m) % self.n] ^ xA

        self.index = 0


def randint(mersenne, nr):
    x = mersenne.extract_number()
    return (nr*x) >> 32

charset = "iHRYg79zJXaGw1CF5K0d3vZobhAlx6StUBnjOIMpe2yVuPr4sL8DqmQTkEcWNf"
seed = random.randint(0, 1000*3600*24) 

if __name__ == "__main__":
    mersenne = Mersenne(seed)
    for nr in range(100):
        domain = ""
        for i in range(10):
            c = charset[randint(mersenne, len(charset))]
            domain += c
        domain += ".com"
        print(domain)


