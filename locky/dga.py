import argparse 
from datetime import datetime

config = {
1: {
    # md5: b28da1f2a5d889594a0e77e0853bcf29
    # sha256: 34bd23cbb9cf301ba444e1696694527ffc59edaba2bbbe25c4ac28a90df6f52a
    # sample: https://malwr.com/analysis/OTE2NzIwODkxMWUzNDBlNzhmNGZlMmFjY2ExOWEyZjQ/
    'seed': 62,
    'c1': 0xB11924E1,
    'c2': 0x1BF5,
    'c3': 0x27100001,
    'c4': 0x2709A354,
    'tlds': ['ru', 'pw', 'eu', 'in', 'yt', 'pm', 'us', 'fr', 'de',
        'it', 'be', 'uk', 'nl', 'tf']
    }
}

def ror32(v, s):
    v &= 0xFFFFFFFF
    return ((v >> s) | (v << (32-s))) & 0xFFFFFFFF

def rol32(v, s):
    return ((v << s) | (v >> (32-s))) & 0xFFFFFFFF

def dga(date, config_nr, domain_nr): 
    c = config[config_nr]

    t = ror32(c['c1']*(date.year + c['c2']), 7)
    t = ror32(c['c1']*(t + c['seed'] + c['c3']), 7)
    t = ror32(c['c1']*(t + (date.day//2) + c['c3']), 7)
    t = ror32(c['c1']*(t + date.month + c['c4']), 7)

    nr = rol32(domain_nr % 8, 21)
    s = rol32(c['seed'], 17)

    r = (ror32(c['c1']*(nr + t + s + c['c3']), 7) + c['c3']) & 0xFFFFFFFF

    length = (r % 11) + 5

    domain = ""
    for i in range(length):
        r = (ror32(c['c1']*rol32(r, i), 7) + c['c3']) & 0xFFFFFFFF
        domain += chr(r % 25 + ord('a'))
    domain += '.'
    r = ror32(r*c['c1'], 7)
    tlds = c['tlds']
    tld_i = (r + c['c3']) % len(tlds)
    domain += tlds[tld_i]
    return domain




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", 
            help="date for which to generate domains")
    parser.add_argument("-c", "--config", choices=[1],
            help="config nr", type=int, default=1)
    args = parser.parse_args()

    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()

    for i in range(8):
        print( dga(d, args.config, i) )
            
