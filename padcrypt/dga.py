"""
    The DGA of Padcrypt 
"""

import argparse
import hashlib
from datetime import datetime

configs = {
    1 : {
        'nr_domains': 24,
        'tlds': ['com', 'co.uk', 'de', 'org', 'net', 'eu', 'info', 'online',
            'co', 'cc', 'website'],
        'digit_mapping': "abcdnfolmk"
        }
}

def dga(date, config_nr):
    config = configs[config_nr]
    dm = config['digit_mapping']
    tlds = config['tlds']
    for i in range(config['nr_domains']):
        seed_str = "{}-{}-{}:{}".format(date.day, date.month, date.year, i)
        h = hashlib.sha256(seed_str.encode('ascii')).hexdigest()
        domain = ""
        for hh in h[3:16+3]:
            domain += dm[int(hh)] if '0' <= hh <= '9' else hh
        tld_index = int(h[-1], 16)
        tld_index = 0 if tld_index >= len(tlds) else tld_index
        domain += "." + config['tlds'][tld_index]
        yield domain

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    parser.add_argument("-c", "--config", help="config", choices=[1], 
            default=1, type=int)
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    for domain in dga(d, args.config): 
        print(domain)
