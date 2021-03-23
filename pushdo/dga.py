import hashlib
import struct
import argparse
from datetime import datetime
from itertools import chain


configs = {
    "kz_v1": {
        "conso_a": "bcdfghjklmnpqrstvwx",
        "conso_b": "zxtsrqpnmlkgfdc",
        "vowels_a": "aeiou",
        "vowels_b": "aio",
        "mod": 7,
        "mod2": 1,
        "tld": "kz"
    },
    "com_v1": {
        "conso_a": "bcdfghjklmnpqrstvwx",
        "conso_b": "zxtsrqpnmlkgfdc",
        "vowels_a": "aeiou",
        "vowels_b": "aio",
        "mod": 7,
        "mod2": 1,
        "tld": "com"
    }, 
    "kz_v2": {
        "conso_a": "kqbhcndjfwglpmzxrsv", 
        "conso_b": "qzlbtgrnkxsfdcm",
        "vowels_a": "aeiou",
        "vowels_b": "aio",
        "mod": 8,
        "mod2": 2,
        "tld": "kz"
    }
}


def part(r, c):
    config = configs[c]
    mod = config.get("mod")
    mod2 = config.get("mod2")
    conso_a = config.get('conso_a')
    conso_b = config.get('conso_b')
    vowels_a = config.get('vowels_a')
    vowels_b = config.get('vowels_b')
    assert(len(conso_a) == 19)
    assert(len(vowels_a) == 5)
    assert(len(vowels_b) == 3)
    assert(len(conso_b) == 15)

    string = ""
    string += conso_a[r % 19]
    rp2 = r + 2
    string += vowels_a[((r+1) & 0xFF) % 5]
    if string[1] == 'e' and rp2 & mod:
        v = vowels_b[rp2 % 3]
    else:
        if not (rp2 & mod2):
            return string
        v = conso_b[(r+3) % 15]
    string += v
    return string


def dga(md5, length, config, loops=16):
    domain = ""
    for i in range(loops):
        r = md5[i]
        p = part(r, config)
        domain += p
        if len(domain) >= length:
            domain = domain[:length]
            domain += ".kz"
            return domain


def days_since_0(d):
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year = d.year
    month = d.month - 1
    day = d.day
    if not year % 4:
        days_in_month[1] = 29
    t = 0
    while month > 0:
        t += days_in_month[month]
        month -= 1
    return day + t + 365*(year - year//4) + 366*(year//4)


def domains_for_day(r, config):
    for i in range(30):
        b = struct.pack("<I", r)
        md5 = hashlib.md5(b).digest()
        r = struct.unpack("<I", md5[:4])[0]
        length = (r & 3) + 9
        domain = dga(md5, length, config)
        r += 1
        yield(domain)


def generate_domains(date, config):
    days = days_since_0(date)
    for j in chain(range(0, -31, -1), range(1, 15)):
        yield from domains_for_day(days + j, config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gozi dga")
    parser.add_argument("-c", "--config", default="kz_v1", choices=list(configs.keys()))
    parser.add_argument("-d", "--date", 
            help="date for which to generate domains")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    for domain in generate_domains(d, args.config):
        print(domain)
