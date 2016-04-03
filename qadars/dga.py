import argparse
import time
from datetime import datetime
import time
import string

def rand(r):
    return  (35317 - 1043968403*r) & 0x7FFFFFFF

def dga(date):
    charset = string.ascii_lowercase + string.digits
    tlds = [".com", ".org", ".net"]
    unix = int(time.mktime(date.timetuple()))
    b = 7*24*3600
    c = 3*24*3600
    r = ( (unix//b)*b - c) & 0x7FFFFFFF

    for i in range(200):
        domain = "" 
        for _ in range(12):
            r = rand(r)
            domain += charset[r % len(charset)]
        r = rand(r)
        tld = tlds[r % 3]
        domain += tld
        print(domain)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", 
            help="date for which to generate domains")
    args = parser.parse_args()

    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    dga(d)
            
