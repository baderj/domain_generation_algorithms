import base64
import argparse
from datetime import datetime, timedelta
import string
import itertools

def encode(plain: str, key: bytes):
    # base64 encode
    plain = plain.encode('ascii')
    plain = base64.urlsafe_b64encode(plain).decode('ascii')
    tmp = bytearray()



    # XOR encrypt
    for p, k in zip(plain, itertools.cycle(key)): 
        if p in string.ascii_letters:
            p =  p.swapcase()
        c = ord(p) ^ k 
        tmp.append(c)

    # base64 encode
    cipher = base64.urlsafe_b64encode(tmp).decode('ascii')

    # strip padding
    cipher = cipher.rstrip("=")

    # reverse
    tmp = cipher[::-1]
    return tmp


def dga(seed: str, date: datetime):
    ds = date.strftime("%Y%d")
    sld = encode(ds, seed.encode('ascii'))
    return f"{sld}.com"


if __name__=="__main__":
    parser = argparse.ArgumentParser()    
    parser.add_argument(
        "-d", "--date", 
        help="date for which to generate domains"
    )
    parser.add_argument('-s', '--seed', help='seed for the dga', default="Crackalackin'")
    parser.add_argument('-n', '--nr', help='how many days into the future to generate domains', type=int, default=1)
    args = parser.parse_args()

    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()

    for i in range(args.nr):
        print(dga(args.seed, d))
        d += timedelta(days=1)
