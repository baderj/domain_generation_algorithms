"""
    Time-Dependent DGA of Tempedreve
    --------------------------------
    sample: https://www.virustotal.com/en/file/6d0f7460569993ffeedfb67514f50e1d93b7124e132f0de6bb3f57d00d779c9d/analysis/1493892364/
    md5: a1310a8d9a6a51be4a6600a2be7ddab2


    This DGA is very similar to the time-independent one described
    by Anubis Networks, see
    https://www.anubisnetworks.com/tempedreve-botnet-report
"""

import string
import argparse
from datetime import datetime, timedelta

def rand(r):
    r = (16843009 * r) & 0xFFFFFFFF
    r = (r + 65805) & 0xFFFFFFFF
    return r

def shuffle(letters, seed):
    r = seed;
    for j in range(len(letters)): 
        i = r % len(letters) 
        r = rand(r) 
        letters[j], letters[i] = letters[i], letters[j]
    return letters

def dga(d):
    enddate = datetime.strptime("2015-03-23", "%Y-%m-%d")
    while d >= enddate:
        days = days_since_unix_epoch(d)
        seed = (((1664525*days) & 0xFFFFFFFF) + 1013904223) & 0xFFFFFFFF
        tlds = ['.com', '.net', '.org', '.info']
        letters = list(string.ascii_lowercase)
        letters = shuffle(letters, seed)
        length = seed % 5 + 7
        domain = ""
        r = seed
        for i in range(length):
            domain += letters[r % len(letters)]
            r = rand(r)
        tld = tlds[seed & 3]
        domain += tld
        d -= timedelta(days=1)
        yield domain

def days_since_unix_epoch(dt):
    return (dt - datetime(1970,1,1)).days

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    for domain in dga(d):
        print(domain)
