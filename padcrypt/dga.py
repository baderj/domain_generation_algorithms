"""
    The DGA of PadCrypt 

    See 
    - https://twitter.com/BleepinComputer/status/705813885673201665
    - http://www.bleepingcomputer.com/news/security/padcrypt-the-first-ransomware-with-live-support-chat-and-an-uninstaller/
    - http://www.bleepingcomputer.com/news/security/the-padcrypt-ransomware-is-still-alive-and-kicking/
    - http://johannesbader.ch/2016/03/the-dga-of-padcrypt/

"""

import argparse
import hashlib
from datetime import datetime

configs = {
    "2.2.86.1" : {
        'nr_domains': 24,
        'tlds': ['com', 'co.uk', 'de', 'org', 'net', 'eu', 'info', 'online',
            'co', 'cc', 'website'],
        'digit_mapping': "abcdnfolmk",
        'separator': ':',
        },
    "2.2.97.0" : {
        'nr_domains': 24*3,
        'tlds': ['com', 'co.uk', 'de', 'org', 'net', 'eu', 'info', 'online',
            'co', 'cc', 'website'],
        'digit_mapping': "abcdnfolmk",
        'separator': '|'
        }
}

def dga(date, config_nr):
    config = configs[config_nr]
    dm = config['digit_mapping']
    tlds = config['tlds']
    for i in range(config['nr_domains']):
        seed_str = "{}-{}-{}{}{}".format(date.day, date.month, date.year,
                config['separator'], i)
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
    parser.add_argument("-v", "--version", help="dga version", 
            choices=["2.2.86.1", "2.2.97.0"], default="2.2.86.1")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    for domain in dga(d, args.version): 
        print(domain)
