import hashlib
from datetime import datetime
import argparse


def dga(date):

    for index in range(1000):
        seed = 7*[0]
        seed[0] = ((date.year & 0xFF) + 0x30) & 0xFF
        seed[1] = date.month 
        seed[2] = (date.day//7)*7
        r = index
        for i in range(4):
            seed[3+i] = r & 0xFF
            r >>= 8

        seed_str = ''.join([chr(s) for s in seed])

        md5 = hashlib.md5(seed_str).digest()

        domain = ""
        for m in md5:
            """ 
                a:   'a' ... 'p' 
                b:   'q' ... 'z' . '1' ... '6' 
                c:   '0' ... '9' IFF b is a number, else discard
            """
            m = ord(m)
            a = (m & 0xF) + ord('a') 
            b = (m >> 4) + ord('q') 
            if b > ord('z'): 
                b = b - ord('J') 
                c = (a % 10) + ord('0')
            else:
                c = None

            domain += chr(a)
            domain += chr(b)
            if c:
                domain += chr(c)

        tlds = [".ru", ".biz", ".info", ".org", ".net", ".com"]
        for i, tld in enumerate(tlds): 
            m = len(tlds) - i
            if not index % m: 
                domain += tld
                break
        print(domain)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    dga(d)
