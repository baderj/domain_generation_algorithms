import argparse
from datetime import datetime

r = 0x1DB98930
len_l = 0xC
len_u = 0x18


def init_rand_and_chars(year, month, day, nr_b):
    global r
    r = (r + year + ((nr_b << 16) + (month << 8) | day)) & 0xFFFFFFFF
    charset = [chr(x) for x in xrange(ord('a'), ord('z'))] +\
            [chr(x) for x in xrange(ord('0'), ord('9'))]
            
    return charset

def generate_domain(charset):
    global r
    r = (1664525*r + 1013904223) & 0xFFFFFFFF
    domain_len = len_l + r % (len_u - len_l)
    domain = ""
    for i in range(domain_len, 0, -1):
        r = ((1664525 * r) + 1013904223) & 0xFFFFFFFF
        domain += charset[r % len(charset)] 
    domain += ".ddns.net"
    print(domain)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    parser.add_argument("-n", "--nr", help="nr of domains to generate", type=int, default=40)
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()

    charset = init_rand_and_chars(d.year, d.month, 8, 1) 
    for _ in range(40):
        generate_domain(charset)
    
    
