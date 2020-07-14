import argparse
from datetime import datetime
from itertools import product


def dga(date):
    month = date.month
    year = date.year
    date_str = "{0:02d}{1:04d}".format(12-month, year-18)

    valid_chars = [
      "]^_`abcde",
      "`abcdef",
      "bcdefgh",
      "efghi",
      "ghijk",
      "ijklm"
    ]
    valid_chars = [list(_) for _ in valid_chars]
    for part1 in product(*valid_chars):
        domain = "".join(part1)
        for i, c in enumerate(part1):
            r = ord(c) + int(date_str[i])
            if r < ord('a'):
                domain += 'z'
            else:
                domain += chr(r)
        domain += ".bazaar"
        yield domain



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date when domains are generated, e.g., 2020-06-28")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    for domain in dga(d):
        print(domain)
