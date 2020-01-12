from datetime import datetime
import hashlib
import argparse

tlds = [
    ".org",
    ".tickets",
    ".blackfriday",
    ".hosting",
    ".feedback",
]

magic = "jkhhksugrhtijys78g46"
special = "31b4bd31fg1x2"


def dga(date, back=0):
    epoch = datetime(1970, 1, 1)
    days_since_epoch = (date - epoch).days
    days = days_since_epoch
    for j in range(back+1):
        for nr in range(500):
            for tld in tlds:
                seed = "{}-{}-{}".format(magic, days, nr)
                m = hashlib.md5(seed.encode('ascii')).hexdigest()
                mc = m[:13]
                if nr == 0:
                    sld = special
                else:
                    sld = mc

                domain = "{}{}".format(sld, tld)
                yield domain
        days -= 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date when domains are generated")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    for domain in dga(d):
        print(domain)
