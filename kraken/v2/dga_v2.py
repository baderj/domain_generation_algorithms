import time
import argparse
from datetime import datetime

def rand(r):
    t =  (1103515245 * r + 12435) & 0xFFFFFFFF
    return t

def crop(r):
    return (r // 256)  % 32768 

def dga(index, date, seed_set, temp_file=True, tld_set_nr=1):
    tld_sets = {1: ["com", "net", "tv", "cc"],
                2: ["dyndns.org", "yi.org", "dynserv.com", "mooo.com"]}

    seeds = {'a': {'ex': 24938314 , 'nex': 24938315 }, 
             'b': {'ex': 1600000, 'nex': 1600001}}
    tlds = tld_sets[tld_set_nr] 

    domain_nr = int(index/2)
    if temp_file:
        r = 3*domain_nr + seeds[seed_set]['ex']
    else:
        r = 3*domain_nr + seeds[seed_set]['nex']


    discards = (int(time.mktime(date.timetuple())) - 1207000000) // 604800  + 2
    if domain_nr % 9 < 8:
        if domain_nr % 9 >= 6:
            discards -= 1
        for _ in range(discards):
            r = crop(rand(r))

    rands = 3*[0]
    for i in range(3):
        r = rand(r)
        rands[i] = crop(r)
    domain_length = (rands[0]*rands[1] + rands[2]) % 6 + 7
    domain = ""
    for i in range(domain_length):
        r = rand(r)
        ch = crop(r) % 26 + ord('a')
        domain += chr(ch)
    domain += "." + tlds[domain_nr % 4]
    return domain

def get_domains(nr, date, seed, tld_set):
    domains = []
    for i in range(nr):
        for temp_file in range(2):
            domains.append(dga(i*2, date, seed, temp_file, tld_set))
    return domains

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", 
            help="date for which to generate domains")
    parser.add_argument("-t", "--tld", choices=[1,2], type=int,
            help="tld set", default=1)
    parser.add_argument('-s', '--seed', choices=['a','b'], default='a')
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    for domain in get_domains(1000, d, args.seed, args.tld):
        print(domain)
