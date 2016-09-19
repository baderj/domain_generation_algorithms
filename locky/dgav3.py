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
2: {
    # md5: 5fb8f8f75342ff68ed8c79cc375f0cd8
    # sha256: bc7c45b5a05f3f0deea162578e45d5fb64c9aa72a81395083509c0f78b6ae1de
    # sample: https://malwr.com/analysis/NzFlYzRkOWZhZDliNDZmMThkMzkzMjU2ZmE5ODUzMjE/
    'seed': 5566,
    'shift': 7,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
3: {
    # md5: 19079496f6abfafd9a99d02098556a79
    # sha256: 5dd6188efe13268bb9ac20ecdb257085e7d62163
    # sample: https://malwr.com/analysis/Yzg5ZWMyZDZmNGFhNGU0YWJjMzY3YjBmMjY4Y2JlMDM/
    'seed': 9106,
    'shift': 7,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
4: {
    # md5: 0e223d578eaddec361498591ec8c1a19
    # sha256: 
    # sample: 
    'seed': 5579,
    'shift': 7,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
5: {
    # md5: 6cb11f4066f74556dd14d27008d867b4
    # sha256: 353ea18baa6c9c796a7b48bcccbf4c9c3c6aa63f8b4dd55d796c65e22028b77b
    # sample: https://malwr.com/analysis/N2Q4YWUyM2I3Y2VlNGQwYzllMjczNzE2Njc1ZTFhZWI/
    'seed': 111,
    'shift': 7,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
6: {
    # md5: ed534695e79a2a70e8b15f8873cdfa02
    # sha256:  
    # sample: https://www.sophos.com/en-us/threat-center/threat-analyses/viruses-and-spyware/Troj~Ransom-CUL/detailed-analysis.aspx
    'seed': 9044,
    'shift': 7,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
7: {
    # md5: bfb5fec661318f07b0eca8520bb8c53f 
    # sha256:  92a1d459194d0bf86ff26103a9c92d64059e1caa9d98e1ed9002058a0da8f53d
    # sample: https://malwr.com/analysis/Mzc0MTU0MTQ1YjRlNGVhYzgzMmQ0MGQ3YWY1NWUzZDg/
    'seed': 9099,
    'shift': 7,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
8: {
    # md5: a075610a69e196ab74f79508dbcf5eef
    # sha256: caa6e59e98c22a3f9159412a612ad170d2683640e1845afb6f533f279f5e6577
    # sample: https://malwr.com/analysis/OWJhZjQ5ZmE4YjY4NDFhYmFhNjIxZDcyYmFkYzlhYTM/
    'seed': 9047,
    'shift': 7,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
9: {
    # md5: 6c3e68307d01e4340c83fac94f237237  
    'seed': 9133,
    'shift': 7,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
10: {
    # md5:  17bf0d1776de896315cb2d63118f9667
    # sha256: 98d6ebd37c861beaf7420494aa8dfd43e4904145bac62c607965b3a8d92967c1
    # sample: https://malwr.com/analysis/NWJiNjJhZWU2YjU2NGRlYjg5Njk2ZGJlMzZkZDcxYWI/
    'seed': 9199,
    'shift': 7,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
11: {
    # md5:  
    # sha256: 
    # sample: 
    'seed': 9190,
    'shift': 7,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
12: {
    # md5:
    # sha256:
    # sample: https://malwr.com/analysis/NzY4YmRjZDA1MTYwNGEzMzg2MWZkNmUyODIzMWRhMDM/
    'shift': 7,
    'seed': 9088,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
13: {
    # md5: 6eb8865bf055ba30cc9e2843f16ee461
    # sha256:
    # sample: 
    'shift': 7,
    'seed': 9998,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
14: {
    # md5: b5660f65369abc67cfa4a65e7d0d65d9
    # sha256: 478ab3b1f465dc1088b0d1e7cef8cab1f3b736856f6be279d4e7a8113ad065d5
    # sample: https://www.virustotal.com/en/file/478ab3b1f465dc1088b0d1e7cef8cab1f3b736856f6be279d4e7a8113ad065d5/analysis/
    'shift': 7,
    'seed': 9992,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
15: {
    # md5: aceec3d6334e925297efc8d4232473c2
    # sha256: 5c18ab258a3a89980aaa9d673a07851fcab4443733a00c4fbf14d21906b65c9e
    # sample: https://www.virustotal.com/en/file/5c18ab258a3a89980aaa9d673a07851fcab4443733a00c4fbf14d21906b65c9e/analysis/1463993646/
    'shift': 7,
    'seed': 1511,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
16: {
    # md5: 
    # sha256: 
    # sample: (downloaded by) https://malwr.com/analysis/ODU3OWM4ZDMxMmE2NDllZWE4MWQ3ZGQ2ZTBjZTc4MWI/
    'shift': 7,
    'seed': 1513,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
17: {
    # md5: 89f35a5d22088e3ca8664697e895b7a5 
    # sha256: 
    # sample: 
    'shift': 7,
    'seed': 1517,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
18: {
    # md5: a9d09406e0982d652b6db291558df71a 
    # sha256: 
    # sample: 
    'shift': 7,
    'seed': 9056,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
19: {
    # md5:  
    # sha256: 
    # sample: 
    # ref: https://nominum.com/locky-back/
    'shift': 7,
    'seed': 7773,
    'tlds': ['ru', 'info', 'biz', 'click', 'su', 'work', 'pl', 'org', 'pw',
        'xyz']
    },
20: {
    # md5:  
    # sha256: 
    # sample: 
    # ref: https://nominum.com/locky-back/
    'shift': 7,
    'seed': 7743,
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
    tld_i = ((k + 0x27100001) & 0xFFFFFFFF) % len(tlds)
    domain += tlds[tld_i]
    return domain



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", 
            help="date for which to generate domains")
    parser.add_argument("-c", "--config", choices=range(1,len(config)+1),
            help="config nr", type=int, default=1)
    args = parser.parse_args()

    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()

    for i in range(12):
        print( dga(d, args.config, i) )
            
