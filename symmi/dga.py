import argparse
from  datetime import datetime

seed_const = 42
days_period = 16
nr_of_domains = 64
third_lvl_min_len = 8
third_lvl_max_len = 15

class Rand:

    def __init__(self, seed):
        self.seed = seed

    def rand(self):
        self.seed = (self.seed*214013 + 2531011) & 0xFFFFFFFF
        return (self.seed >> 16) & 0x7FFF


def next_domain(r, second_and_top_lvl, third_lvl_domain_len):
    letters = ["aeiouy", "bcdfghklmnpqrstvwxz"]
    domain = ""

    for i in range(third_lvl_domain_len):
        if not i % 2:
            offset_1 = 0 if r.rand() & 0x100 == 0 else 1
        s = r.rand()
        offset = (offset_1 + i) % 2
        symbols = letters[offset]
        domain += symbols[s % (len(symbols) - 1)]

    return domain + second_and_top_lvl

def dga(seed, second_and_top_lvl, nr):
    r = Rand(seed)
    for i in range(nr):
        span = third_lvl_max_len - third_lvl_min_len + 1
        third_lvl_len = third_lvl_min_len + r.rand() % span
        print(next_domain(r, second_and_top_lvl, third_lvl_len))

def create_seed(date):
    return 10000*(date.day//days_period*100 + date.month) + date.year + seed_const

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="as YYYY-mm-dd")
    args = parser.parse_args()
    date_str = args.date
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = datetime.now() 
    seed = create_seed(date)
    dga(seed, ".ddns.net", nr_of_domains)
