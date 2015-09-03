import json
import argparse
from datetime import datetime
import time


def get_sld(length, seed):
    sld = ""
    modulo = 541 * length + 4
    a = length * length
    for i in range(length):
        index = (a + (seed*((seed % 5) + (seed % 123456) +
            i*((seed & 1) + (seed % 4567))) & 0xFFFFFFFF))  % 26
        a += length;
        a &= 0xFFFFFFFFF
        sld += chr(ord('a') + index)
        seed += (((7837632 * seed * length) & 0xFFFFFFFF) + 82344) % modulo;
    return sld


def generate_domains(date, nr, set_nr):
    with open("set{}_seeds.json".format(set_nr), "r") as r:
        seeds = json.load(r)
    dt = time.mktime(date.timetuple())
    days = 20 if set_nr == 1 else 1
    index = int(dt//(days*3600*24))
    if str(index) not in seeds:
        print("Sorry, {} is out of the time range I know".format(date))
        return
    seed = int(seeds.get(str(index), None), 16)
    original_seed = seed 

    for dga_nr in range(nr):
        # determine next seed
        s = seed % (dga_nr + 1)
        seed += (s + 1)
        
        # second level length
        length = (seed + dga_nr) % 7 + 6  

        # get second level domain
        second_level_domain = get_sld(length, seed)

        # get first level domain
        tlds = ['com', 'net', 'org', 'info', 'cc']
        top_level_domain = tlds[(seed & 3)]

        # concatenate and print domain
        domain = second_level_domain + '.' +  top_level_domain
        print(domain)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    parser.add_argument("-n", "--nr", help="nr of domains to generate", type=int, default=10)
    parser.add_argument("-s", "--set_nr", help="seeds set, 1 = useful dga, 2 = noise dga",
            type=int, default=1, choices=[1,2])
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    generate_domains(d, args.nr, args.set_nr)
