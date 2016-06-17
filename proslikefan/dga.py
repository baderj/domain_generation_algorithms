import argparse
from ctypes import c_int
from datetime import datetime

def dga(date, magic, tlds):
#    tlds = ["eu", "biz", "se", "info", "com", "net", "org", "ru", "in", 
#            "name"]
    for i in range(10):
        for tld in tlds:
            seed_string = '.'.join([str(s) for s in 
                    [magic, date.month, date.day, date.year, tld]])
            r = abs(hash_string(seed_string)) + i
            domain = ""
            k = 0
            while(k < r % 7 + 6):
                r = abs(hash_string(domain + str(r))) 
                domain += chr(r % 26 + ord('a')) 
                k += 1
            domain += '.' + tld
            print(domain)


def hash_string(s):
    h = c_int(0) 
    for c in s:
        h.value = (h.value << 5) - h.value + ord(c)
    return h.value


if __name__=="__main__":
    """ known magic seeds are "prospect" and "OK" """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    parser.add_argument("-m", "--magic", help="magic string", 
            default="prospect")
    parser.add_argument("-t", "--tlds", nargs="+", help="tlds",
        default=["eu", "biz", "se", "info", "com", "net", "org", "ru", "in", "name"])
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    dga(d, args.magic, args.tlds)
