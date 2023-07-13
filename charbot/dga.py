############
# CharBot implemetation from the paper in https://arxiv.org/abs/1905.01078
#
# When checking, I'm getting ~0% of registered domains, in agreement with the paper which says 
# the algorithm generates 100% valid DGA domains. 
#

import urllib
import dns.resolver
import pandas as pd
import numpy as np


def dns_query_specific_nameserver(query="techoverflow.net", nameserver="1.1.1.1", qtype="A"):
    """
    Query a specific nameserver for:
    - An IPv4 address for a given hostname (qtype="A")
    - An IPv6 address for a given hostname (qtype="AAAA")
    
    Returns the IP address as a string
    """
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [nameserver]
    answer = resolver.resolve(query, qtype)
    if len(answer) == 0:
        return None
    else:
        return str(answer[0])

def create_new_domain(check_availability=False):
    real_domain = tranco.sample(1).domain.values[0]
    while len(real_domain.split('.')[0]) < 6:
        real_domain = tranco.sample(1).domain.values[0]
    new_domain = list(real_domain.split('.')[0])

    # index of the chars to replace in the read domain
    i, j = np.random.randint(0,len(new_domain),2)
    # index of the chars to be replaced with
    ci, cj = np.random.randint(0,len(dnscharset),2)
    # index of the TLD
    tdlidx = np.random.randint(len(TLDs))

    new_domain[i] = dnscharset[ci]
    new_domain[j] = dnscharset[cj]
    new_domain += '.'+TLDs[tdlidx]
    new_domain = ''.join(new_domain)

    if check_availability:
        try:
            # if the DNS query returns an IP, then is not valid DGA
            dns_query_specific_nameserver(new_domain)
            valid = 0
            print("Not valid DGA: ",real_domain, new_domain)
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            valid = 1
    else:
        valid = 1
    # returns the sampled domain, the transformed domain and 1 if is a valid DGA or 0 if new_domain is registered
    return [real_domain, new_domain, valid]

if __name__ == '__main__':
    TLDs = 'com, at, uk, pl, be, biz, co, jp, cz, de, eu, fr, info, it, ru, lv, me, name, net, nz, org, us'.split(', ')
    dnscharset = [chr(x) for x in range(0x61, 0x61+26)] + [chr(x) for x in range(0x30, 0x30+10)] + ['-']
    # using the Tranco 1M list from 2023-07-13 as list of good domains.
    if True:     # <---- to False to avoid download tranco every time
        try:
            print('Downloading Tranco List')
            urllib.request.urlretrieve('https://tranco-list.eu/download/25259/1000000', 'tranco1M.csv')
        except urllib.error.URLError as e:
            print("Can't download the tranco list")
            raise e

    np.random.seed(42)
    tranco = pd.read_csv('tranco1M.csv', names=['ranking', 'domain'])

    # create 1000 valid domains
    domains = []
    print('Generating domains')
    for _ in range(1000):
        # Can take some time, as will query almost 1000 non existing domains
        dga = create_new_domain(check_availability=True)
        if dga[2] == 1:
            domains.append(dga)
    df = pd.DataFrame(domains, columns=['real', 'charbot', 'valid'])
    df.to_csv('domains_examples.txt', columns=['charbot'], index=False)
