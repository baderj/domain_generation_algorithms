from datetime import datetime
import argparse
from ctypes import c_int

def prng(seed_string):
    result = c_int()
    for c in seed_string:
        a = result.value 
        result.value = (result.value << 5)
        tmp = result.value - a
        result.value = tmp + ord(c)
        result.value &= result.value

    return result.value

def dga(seed, d):
    tlds = ["cc", "co", "eu"]
    dga_domains = []
    for i in range(10):
        for j, tld in enumerate(tlds):
            ss = ".".join([str(s) for s in [seed, d.month, d.day, d.year, tld]])
            r = abs(prng(ss)) + i
            domain = ""
            k = 0
            while k < (r % 7 + 6):
                r = abs(prng(domain + str(r)))
                domain += chr(r % 26 + ord('a'))
                k += 1
            dga_domains.append("{}.{}".format(domain, tld))
    return dga_domains

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--seed", help="seed", default="OK")
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    args = parser.parse_args()
    
    d = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.now()

    for domain in dga(args.seed, d):
        print(domain)
