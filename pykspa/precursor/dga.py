from datetime import datetime
import argparse
from time import mktime

def get_sld(sld_len, r):
    a = sld_len ** 2
    sld = ""
    for i in range(sld_len):
        x = i*(r % 4567 + r % 19) & 0xFFFFFFFF
        y = r % 123456
        z = r % 5
        p = (r*(z + y + x)) & 0xFFFFFFFF
        ind = (a + p) & 0xFFFFFFFF
        sld += chr(ord('a') + ind % 26)
        r = (r + i) & 0xFFFFFFFF
        r = r >> (((i**2) & 0xFF) & 31 ) 
        a += sld_len
        a &= 0xFFFFFFFF
    return sld

def dga(seed, nr_domains = 5000):
    tlds = ["biz", "com", "net", "org", "info", "cc"]
    r = seed
    for domain_nr in range(nr_domains):
        r = int(r ** 2) & 0xFFFFFFFF
        r += domain_nr
        r &= 0xFFFFFFFF
        domain_length = (r % 10) + 6
        sld = get_sld(domain_length, r)
        tld = tlds[r % 6]
        domain = "{}.{}".format(sld, tld)
        print(domain)


def generate_domains(date, nr):
    unix_timestamp = mktime(date.timetuple())
    seed = int(unix_timestamp // (2*24*3600) )
    date_range = [] 
    for i in range(2):
        ts = (seed+i)*2*24*3600
        date_range.append(datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M"))
    t = "pykspa domains valid through {} - {}".format(*date_range)
    print("{}\n{}".format(t, "*"*len(t)))
    dga(seed, nr)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    parser.add_argument("-n", "--nr", help="nr of domains to generate", type=int, default=5000)
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    generate_domains(d, args.nr)
