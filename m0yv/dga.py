import argparse

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


def dga(seed):
    for i in range(128):
        r = Rand(seed ^ i)
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
    args = parser.parse_args()
    for domain in dga(args.seed):
        print(domain)
