from datetime import datetime
from ctypes import c_uint
import argparse


seeds = {
        'luther': {'div': 4, 'tld': '.com', 'nr': 12},
        'rfc4343': {'div': 3, 'tld': '.com', 'nr': 10},
        'nasa': {'div': 5, 'tld': '.com', 'nr': 12},
        'gpl': {'div': 5, 'tld': '.ru', 'nr': 10}
        }
        
        
class Rand:

    def __init__(self, seed):
        self.r = c_uint(seed) 

    def rand(self):
        self.r.value = 1664525*self.r.value + 1013904223
        return self.r.value

def get_words(wordlist):
    with open(wordlist, 'r') as r:
        return [w.strip() for w in r if w.strip()]

def dga(date, wordlist):
    words = get_words(wordlist)
    diff = date - datetime.strptime("2015-01-01", "%Y-%m-%d")
    days_passed = (diff.days // seeds[wordlist]['div'])
    flag = 1
    seed = (flag << 16) + days_passed - 306607824
    r = Rand(seed) 

    for i in range(12):
        r.rand()
        v = r.rand()
        length = v % 12 + 12
        domain = ""
        while len(domain) < length:
            v = r.rand() % len(words)
            word = words[v] 
            l = len(word)
            if not r.rand() % 3:
                l >>= 1
            if len(domain) + l <= 24:
                domain += word[:l]
        domain += seeds[wordlist]['tld']
        yield domain

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gozi dga")
    parser.add_argument("-d", "--date", 
            help="date for which to generate domains")
    parser.add_argument("-w", "--wordlist", help="wordlist", 
            choices=list(seeds.keys()), default='luther')
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()

    for domain in dga(d, args.wordlist):
        print(domain)
