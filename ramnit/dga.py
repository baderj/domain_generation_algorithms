import argparse

class RandInt:

    def __init__(self, seed): 
        self.seed = seed

    def rand_int_modulus(self, modulus):
        ix = self.seed                
        ix = 16807*(ix % 127773) - 2836*(ix / 127773) & 0xFFFFFFFF        
        self.seed = ix 
        return ix % modulus 

def get_domains(seed, nr):
    r = RandInt(seed)

    for i in range(nr):
        seed_a = r.seed
        domain_len = r.rand_int_modulus(12) + 8
        seed_b = r.seed
        domain = ""
        for i in range(domain_len):
            char = chr(ord('a') + r.rand_int_modulus(25))
            domain += char
        domain += ".com"
        m = seed_a*seed_b
        r.seed = (m + m//(2**32)) % 2**32 
        yield domain

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="generate Ramnit domains")
    parser.add_argument("seed", help="seed as hex")
    parser.add_argument("nr", help="nr of domains", type=int)
    args = parser.parse_args()
    for domain in get_domains(int(args.seed, 16), args.nr):
        print(domain)
