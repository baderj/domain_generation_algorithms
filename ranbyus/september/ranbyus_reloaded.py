"""
    The DGA of Ranbyus as described here:
        http://johannesbader.ch/2015/09/ranbyuss-dga-revisited/

    Known Seeds are:
        - 0F0D5BFA
        - F2C72B14
        - AE8714BE
        - CE7F8514 (= ~ 31807AEB)
        - 572473BB (= ~ A8DB8C44)
        - 17794CF1 (= ~ E886B30E)
        - C0E32524 (= ~ 3F1CDADB)
        - 7CB7966E (= ~ 83486991)
        - 9F90C9E7 (= ~ 606F3618)
        - 8FB8879B (= ~ 70477864)
        - E981684B (= ~ 167E97B4)
"""

import argparse
from datetime import datetime

def to_little_array(val):
    a = 4*[0]
    for i in range(4):
        a[i] = (val & 0xFF)
        val >>= 8
    return a
        
def pcg_random(r): 
    alpha = 0x5851F42D4C957F2D
    inc = 0x14057B7EF767814F

    step1 = alpha*r + inc
    step2 = alpha*step1 + inc
    step3 = alpha*step2 + inc

    tmp = (step3 >> 24) & 0xFFFFFF00 | (step3  & 0xFFFFFFFF) >> 24
    a = (tmp ^ step2) & 0x000FFFFF ^ step2
    b = (step2 >> 32)
    c = (step1 & 0xFFF00000)  | ((step3 >> 32) & 0xFFFFFFFF) >> 12
    d = (step1 >> 32) & 0xFFFFFFFF

    data = 32*[None]
    data[0:4] = to_little_array(a)
    data[4:8] = to_little_array(b)
    data[8:12] = to_little_array(c)
    data[12:16] = to_little_array(d)
    return step3 & 0xFFFFFFFFFFFFFFFF, data

def dga(year, month, day, seed):
    x = (day*month*year) ^ seed
    tld_index = day
    for _ in range(40):
        random = 32*[None]
        x, random[0:16] = pcg_random(x)
        x, random[16:32] = pcg_random(x)

        domain = ""
        for i in range(17):
            domain += chr(random[i] % 25 + ord('a'))
        if seed == 0xCE7F8514:
            tlds =  ["in", "net", "org", "com", "me", "su", "tw", "cc", "pw"]
        else:
            tlds =  ["in", "me", "cc", "su", "tw", "net", "com", "pw", "org"]
        domain += '.' + tlds[tld_index % (len(tlds) - 1)]
        tld_index += 1
        yield domain

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    parser.add_argument("-s", "--seed", help="seed as hex string", default="0F0D5BFA")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    for domain in dga(d.year, d.month, d.day, int(args.seed, 16)):
        print(domain)
