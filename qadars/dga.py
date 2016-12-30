import argparse
import time
from datetime import datetime
import time
import string

def rand(r, seed):
    return  (seed - 1043968403*r) & 0x7FFFFFFF

def dga(date, seed):
    charset = string.ascii_lowercase + string.digits
    if seed == 0xE1F2:
        tlds = [".com", ".org", ".net"]
    else:
        tlds = [".net", ".org", ".top"]
    unix = int(time.mktime(date.timetuple()))
    b = 7*24*3600
    c = 4*24*3600
    r = unix - (unix-c) % b
    for i in range(200):
        domain = "" 
        for _ in range(12):
            r = rand(r, seed)
            domain += charset[r % len(charset)]
        r = rand(r, seed)
        tld = tlds[r % 3]
        domain += tld
        print(domain)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", 
            help="date for which to generate domains")
    parser.add_argument("-s", "--seed",
            help="seed as hexstring", choices={"89f5", "4449", "E1F2"},
            default="e08a")
    args = parser.parse_args()

    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    dga(d, int(args.seed,16))
            
