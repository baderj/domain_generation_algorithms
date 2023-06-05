"""
    Unknown Malware generating 50 DGA domains

    Variant with Prefix "sn":

    md5:    af650c822feea20ed0b2c99d28007fa3
    sha1:   5adfd2e014a58e1798131ff7644d8df6aa2ecaa5
    sha256: f21f30279ab4b3d4cf090dc51f199f454d3d42df71223eb67b7481efeef8715f

    Variant with Prefix "al":

    md5:    c05c4c97be77270bd0ea916fbb9e9d6d
    sha1:   ed6339ff829e54cd813b81c952ce2970b08819d1
    sha256: 92fd43ee62c1551500e4b604d55dcab88424954776d9a1a6074d5084782a486a
"""

import argparse

def half_until_smaller_equal_24(nr):
    while nr > 24:
        nr = nr >> 1
    return nr

def getchar(nr):
    return chr(half_until_smaller_equal_24(nr) + ord('a'))

def gettld(nr):
    index = half_until_smaller_equal_24(nr)  // 5
    return [".com", ".org", ".net", ".ru", ".in"][index]

def dga(prefix):
    if prefix == "sn":
        primes = [1,7,3,5,11,13]
    else:
        primes = [1,3,5,7,11,13]
    for nr in range(1,51):
        domain = prefix 
        for prime in primes: 
            domain += getchar(prime*nr)
        domain += gettld(nr)
        nr += 1
        yield domain


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prefix", choices=["sn", "al"])
    args = parser.parse_args()
    for domain in dga(args.prefix):
        print(domain)
