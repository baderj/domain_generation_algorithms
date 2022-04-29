import argparse
from ctypes import c_uint
from datetime import datetime

class Rand:
    def __init__(self, seed):
        self.seed = seed
        self.r = self.seed

    def rand(self):
        v = (214013 * self.r + 2531011) & 0xFFFFFFFF
        self.r = v
        v = v >> 16
        if v > 0x7FFF:
            v = v - 2 ** 15
        return v

def secret_pool_seed(seed, date):
    year = date.year
    month = date.month
    day = date.day

    ret = seed + year
    week = (30.5 * month - date.day) / 7.0
    week = c_uint(int((30.5 * month - date.day) / 7.0))

    for c in range(week.value):
        ret = lrotl(ret + 1, 1)

    return ret


def lrotl(value, shift):
    MASK = 0xFFFFFFFF
    overflow = ((value << shift) >> 32) & MASK
    value = (value << shift)
    value += overflow 
    value &= MASK
    return value 

def dga(seed, date):
    for i in range(128):
        s = secret_pool_seed(seed, date) 
        r = Rand(s ^ i)
        k = r.rand()
        l = 5 + k % 5
        domain = ""
        for c in range(l):
            n = r.rand()
            letter = chr(n % 26 + ord("a"))
            domain += letter
        domain += ".biz"

        yield domain

def seed_parser(s):
    return int(s, 0)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    """ known seeds are
        - 0x02484A18
        - 0x00128a0e 
        - 0x7178af3f
    """
    parser.add_argument("-s", "--seed", default=0x2484A18, type=seed_parser)
    parser.add_argument(
        "-d", "--date", 
        help="date for which to generate domains"
    )
    args = parser.parse_args()

    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.utcnow()

    for domain in dga(args.seed, d):
        print(domain)
