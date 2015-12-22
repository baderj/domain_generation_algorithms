import time
from ctypes import c_int, c_uint
import argparse

def rand(r):
    t =  c_int(1103515245 * r + 12435).value
    return t

def crop(r):
    return (r // 256)  % 32768 

def dga(index, seed_set, temp_file=True):

    seeds = {'a': {'ex': -0x0FCFBF88, 'nex': 0x8924541}, 
             'b': {'ex': -0x1FCFBF87, 'nex': 0x7924542}}

    tlds = ["dyndns.org", "yi.org", "dynserv.com", "mooo.com"]
    domain_nr = int(index/2) + 1000015

    if temp_file:
        x = int(c_int(domain_nr*(domain_nr + 7)*(domain_nr+12)).value /9.0) 
        y = domain_nr*(domain_nr+1)
        r = c_int(x + y + seeds[seed_set]['ex']).value 
    else:
        x = int(c_int((domain_nr + 2)*(domain_nr + 7)*domain_nr).value/9.0)
        y = (domain_nr*3 + 1)*domain_nr
        r = c_int(x + y + seeds[seed_set]['nex']).value

    rands = 3*[0]
    for i in range(3):
        r = rand(r)
        rands[i] = crop(r)
    domain_length = (rands[0]*rands[1] - rands[2]) % 6 + 6
    domain = ""
    for i in range(domain_length):
        r = rand(r)
        ch = crop(r) % 26 + ord('a')
        domain += chr(ch)
    domain += "." + tlds[domain_nr % 4]
    return domain

def get_domains(nr, seed_set):
    domains = []
    for i in range(nr):
        for temp_file in range(2):
            domains.append(dga(i*2, seed_set, temp_file))
    return domains

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', choices=['a','b'], default='a')
    args = parser.parse_args()
    for domain in get_domains(1000, args.seed):
        print(domain)
