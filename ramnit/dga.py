import argparse

class RandInt:

    def __init__(self, seed): 
        self.value = seed

    def rand_int_modulus(self, modulus):
        ix = self.value
        ix = 16807*(ix % 127773) - 2836*(ix // 127773) & 0xFFFFFFFF        
        self.value = ix 
        return ix % modulus 

def get_domains(seed, nr, tlds):
    if not tlds:
        tlds = [".com"]

    r = RandInt(seed)

    for i in range(nr):
        seed_a = r.value
        domain_len = r.rand_int_modulus(12) + 8
        seed_b = r.value
        domain = ""
        for j in range(domain_len):
            char = chr(ord('a') + r.rand_int_modulus(25))
            domain += char
        tld = tlds[i % len(tlds)]
        domain += '.' if tld[0] != '.' else ''
        domain += tld
        m = seed_a*seed_b
        r.value = (m + m//(2**32)) % 2**32 
        yield domain

if __name__=="__main__":
    """ 
        example seeds:
            16647BB4
            E7392D18
            C129388E
            E706B455
            DC485593
            EF214BBF
            28488EEA
            4BFCBC6A
            79159C10 
            92F4BE35
            4302C04A 10 -t "click bid eu"
            52278648
            9753029A 100 -t .eu
            A6EAB21A 500
            46CF1B28 500
            1CCEC41C
            0C5787AE2
            0FCFFD9E9
            75EA95C2
            8A0AEC7D
            1DF640A8
            14DF29DD 
            8222270B
            55536A85
            5C39E467
            D2B3C361
            F318D47D
            231D9480
    """
    parser = argparse.ArgumentParser(description="generate Ramnit domains")
    parser.add_argument("seed", help="seed as hex")
    parser.add_argument("nr", help="nr of domains", type=int)
    parser.add_argument("-t", "--tlds", help="list of tlds", default=None)
    args = parser.parse_args()
    tlds = None
    if args.tlds:
        tlds = [x.strip() for x in args.tlds.split(" ")]
    for domain in get_domains(int(args.seed, 16), args.nr, tlds):
        print(domain)
