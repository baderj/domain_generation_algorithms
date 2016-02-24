import binascii
from datetime import datetime
from ctypes import c_uint
import argparse

def date_to_seed(date, seed):
    dx = (date.day-1) // 10 
    data = "{}.{}.{}.{:08x}".format(
            dx if dx <= 2 else 2,
            date.strftime("%b").lower(), 
            date.year, 
            seed)
    crc = c_uint(binascii.crc32(data.encode('ascii')))
    return crc

def _int32(x):
    return int(0xFFFFFFFF & x)

class MT19937:

    def __init__(self, seed):
        # Initialize the index to 0
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = seed  # Initialize the initial state to the seed
        for i in range(1, 624):
            self.mt[i] = _int32(
                1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

    def extract_number(self):
        if self.index >= 624:
            self.twist()

        y = self.mt[self.index]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18

        self.index = self.index + 1
        return _int32(y)

    def twist(self):
        for i in range(0, 624):
            y = _int32((self.mt[i] & 0x80000000) +
                       (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
        self.index = 0

    def rand_int(self, lower, upper):
        r = self.extract_number()
        r &= 0xFFFFFFF
        t = lower + float(r) / (2**28)*(upper - lower + 1) 
        t = int(t)
        return t
        

def dga(date, tlds, nr_domains=5, sandbox=False, seed=0):
    seed = date_to_seed(date, seed).value + sandbox
    mt = MT19937(seed)

    for i in range(nr_domains):
        tld_nr = mt.rand_int(0, len(tlds) - 1)
        length = mt.rand_int(8, 25)
        domain = ""
        for l in range(length):
            domain += chr(mt.rand_int(0, 25) + ord('a'))
        domain += "." + tlds[tld_nr]
        print(domain)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", 
            help="date for which to generate domains")
    parser.add_argument("-s", "--sandbox",
            help="domains when sandbox is detected", action="store_true") 
    parser.add_argument("-n", "--nr",
            help="nr of domains", type=int, default=5000) 
    parser.add_argument("-m", "--seed",
            help="seed", type=int, choices={0,1}, default=0) 
    args = parser.parse_args()

    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()

    tlds = ["com", "net", "org", "info", "biz", "org"]
    dga(d, tlds, args.nr, args.sandbox, args.seed) 
            
