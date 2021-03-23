import hashlib
from datetime import datetime, timedelta
import struct
import argparse

def get_seed(seq_nr, date):
    key = "\x01\x05\x19\x35"
    seq_nr = struct.pack('<I', seq_nr) 
    year = struct.pack('<H', date.year)
    month = struct.pack('<H', date.month)
    day = struct.pack('<H', date.day)
    m = hashlib.md5()
    m.update(seq_nr)
    m.update(year)
    m.update(key.encode('latin1'))
    m.update(month)
    m.update(key.encode('latin1'))
    m.update(day)
    m.update(key.encode('latin1'))
    return m.hexdigest()

def create_domain(seq_nr, date):
    def generate_domain_part(seed, nr):
        part = [] 
        for i in range(nr-1):
            edx = seed % 36
            seed //= 36
            if edx > 9:
                char = chr(ord('a') + (edx-10))
            else:
                char = chr(edx + ord('0'))
            part += char
            if seed == 0:
                break
        part = part[::-1]
        return ''.join(part)    

    def hex_to_int(seed):
        indices = range(0, 8, 2)
        data = [seed[x:x+2] for x in indices]
        seed = ''.join(reversed(data))
        return int(seed,16)

    seed_value = get_seed(seq_nr, date)
    domain = ""
    for i in range(0,16,4):
        seed = seed_value[i*2:i*2+8]
        seed = hex_to_int(seed)
        domain += generate_domain_part(seed, 8)
    if seq_nr % 4 == 0:
        domain += ".com"
    elif seq_nr % 3 == 0:
        domain += ".org"
    elif seq_nr % 2 == 0:
        domain += ".biz"
    else:
        domain += ".net"
    return domain

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    parser.add_argument("-u", "--url", help="search this url in past domains")
    parser.add_argument("-n", "--nr", help="nr of domains to generate")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.today()
    if args.nr:
        nr_of_domains = int(args.nr)
    else:
        nr_of_domains = 1000 
    if args.url:
        while True:
            print("searching in {}".format(d.strftime("%Y-%m-%d")))
            for seq_nr in range(1000):
                domain = create_domain(seq_nr, d)
                if domain == args.url:
                    print("\nfound it, domain nr {} at {}".format(seq_nr,
                        d.strftime("%Y-%m-%d")))
                    break
            if domain == args.url:
                break
            d = d - timedelta(days=1)
    else:
        for seq_nr in range(nr_of_domains):
            domain = create_domain(seq_nr, d)
            print(domain)
