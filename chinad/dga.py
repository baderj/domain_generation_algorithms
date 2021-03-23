import string
import hashlib
import argparse
from datetime import datetime

def dga(date):
    TLDS = ['.com', '.org', '.net', '.biz', '.info', '.ru', '.cn']
    alphanumeric = string.ascii_lowercase + string.digits

    """
        Chinad generates 1000 domains, but only 256 different domains possible
    """
    for nr in range(0x100):
        data = "{}{}{}{}".format(
                chr(date.year % 100),
                chr(date.month),
                chr(date.day),
                chr(nr)) + 12*"\x00" 

        h = hashlib.sha1(data.encode('latin1')).digest()
        h = ''.join(map(chr, h))
        h_le = []
        for i in range(5):
            for j in range(4):
                h_le.append(h[i*4 + (3-j)])

        domain = ""
        for r in h_le[:16]: 
            domain += alphanumeric[(ord(r) & 0xFF) % len(alphanumeric)]

        r = ord(h_le[-4]) 
        domain += TLDS[r % len(TLDS)]
        yield domain

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gozi dga")
    parser.add_argument("-d", "--date", 
            help="date for which to generate domains")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    for domain in dga(d):
        print(domain)
