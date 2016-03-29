import argparse 
from datetime import datetime

config = {
1: {
    # md5: 81e85dcaf482aba2f8ea047145490493
    # sha256: 9afb127e733b01952f00a8174291d39f740b6df2c90d0422b4d6f2e2e6bc7d1a
    # sample: https://virustotal.com/en/file/9afb127e733b01952f00a8174291d39f740b6df2c90d0422b4d6f2e2e6bc7d1a/analysis/
    'seed': 7077,
    'shift': 7,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
}

def ror32(v, s):
    v &= 0xFFFFFFFF
    return ((v >> s) | (v << (32-s))) & 0xFFFFFFFF

def rol32(v, s):
    v &= 0xFFFFFFFF
    return ((v << s) | (v >> (32-s))) & 0xFFFFFFFF

def dga(date, config_nr, domain_nr): 
    c = config[config_nr]
    seed_shifted = rol32(c['seed'], 17)
    dnr_shifted = rol32(domain_nr, 21)

    k = 0
    year = date.year
    for _ in range(7):
        t_0 = ror32(0xB11924E1 * (year + k + 0x1BF5), c['shift']) & 0xFFFFFFFF
        t_1 = ((t_0 + 0x27100001) ^ k) & 0xFFFFFFFF
        t_2 = (ror32(0xB11924E1 * (t_1 + c['seed']), c['shift'])) & 0xFFFFFFFF
        t_3 = ((t_2 + 0x27100001) ^ t_1) & 0xFFFFFFFF
        t_4 = (ror32(0xB11924E1 * (date.day//2 + t_3), c['shift'])) & 0xFFFFFFFF
        t_5 = (0xD8EFFFFF - t_4 + t_3) & 0xFFFFFFFF
        t_6 = (ror32(0xB11924E1 * (date.month + t_5 - 0x65CAD), c['shift'])) & 0xFFFFFFFF
        t_7 = (t_5 + t_6 + 0x27100001) & 0xFFFFFFFF
        t_8 = (ror32(0xB11924E1 * (t_7 + seed_shifted + dnr_shifted), c['shift'])) & 0xFFFFFFFF
        k = ((t_8 + 0x27100001) ^ t_7) & 0xFFFFFFFF
        year += 1

    length = (k % 11) + 7
    domain = ""
    for i in range(length):
        k = (ror32(0xB11924E1*rol32(k, i), c['shift']) + 0x27100001) & 0xFFFFFFFF
        domain += chr(k % 25 + ord('a'))

    domain += '.'
    k = ror32(k*0xB11924E1, c['shift'])
    tlds = c['tlds']
    tld_i = (k + 0x27100001) % len(tlds)
    domain += tlds[tld_i]
    return domain



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", 
            help="date for which to generate domains")
    parser.add_argument("-c", "--config", choices=range(1,2),
            help="config nr", type=int, default=1)
    args = parser.parse_args()

    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()

    for i in range(12):
        print( dga(d, args.config, i) )
            
