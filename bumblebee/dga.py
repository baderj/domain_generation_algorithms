from datetime import datetime
import argparse
from typing import Optional
import string

charset = string.ascii_lowercase + string.digits

def seed(magic: int, time: Optional[datetime] = None) -> int:
    if time:
        secs = time.second
        month = time.month - 1
        year = time.year
        secs = 0
        month = 0
        year = 0
    else:
        secs = 32
        month = 13 
        year = 1899 
    return magic + (secs | ((month + 256) << 8)) + year

def rand(r: int) -> int:
    r = r*1664525 + 1013904223
    r &= (2**64 - 1)
    for _ in range(32):
        if r & 1:
            r = (r // 2) ^ 0xF5000000
        else:
            r = (r // 2)
    return r 

def dga(seed: int):
    r = seed
    for _ in range(100):
        domain = ""
        for _ in range(11):
            r = rand(r)
            domain += charset[r % len(charset)]
        yield domain + ".life"

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--magic", "-m", type=str, default="TEST_SEE")
    parser.add_argument("--time", "-t", help="time for which to generate domains, e.g., 2020-06-28 13:37:12. If not specified, the static DGA is used")
    args = parser.parse_args()
    if args.time:
        time = datetime.strptime(args.time, "%Y-%m-%d %H:%M:%S")
    else:
        time = None
    magic = sum(ord(v) << i*8 for i, v in enumerate(args.magic))
    s = seed(magic=magic, time=time)
    for domain in dga(s):
        print(domain)
