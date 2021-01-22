


def dga(seed, domain, tlds, num_domains):
    seed += (17 - len(seed))*'\x00'
    seed_l = [ord(s) for s in seed]
    yield domain
    for _ in range(num_domains):
        domain_l = [ord(l) for l in domain]
        seed_sum = sum(seed_l[:16])
        new_domain = []
        tmp = seed_l[15] & 0xFF
        for i in range(12):
            while True:
                tmp += domain_l[i]
                tmp ^= (seed_sum & 0xFF)
                tmp += domain_l[i+1]
                tmp &= 0xFF
                if 0x61 < tmp < 0x7a:
                    new_domain.append(tmp)
                    break
                else:
                    seed_sum += 1

        base_domain = ''.join([chr(x) for x in new_domain])
        for tld in tlds:
            domain = base_domain + '.' + tld
            yield domain


if __name__ == '__main__':
    # There are several Tinba variants.  This describes those variations and
    # source references for each.
    dga_configurations = [
        # http://garage4hackers.com/entry.php?b=3086
        ('oGkS3w3sGGOGG7oc', 'ssrgwnrmgrxe.com', ('com',), 1000),
        # https://johannesbader.ch/2015/04/new-top-level-domains-for-tinbas-dga
        ('jc74FlUna852Ji9o', 'blackfreeqazyio.cc', ('com', 'net', 'in', 'ru'), 100),
        # https://www.sophos.com/en-us/threat-center/threat-analyses/viruses-and-spyware/Troj~Tinba-EL/detailed-analysis.aspx
        # https://github.com/baderj/domain_generation_algorithms/commit/c7d154a39bb172c4632f7565e0c9380e8b36c18e
        ('yqokqFC2TPBFfJcG', 'watchthisnow.xyz', ('pw', 'us', 'xyz', 'club'), 100),
        # https://github.com/baderj/domain_generation_algorithms/commit/c7d154a39bb172c4632f7565e0c9380e8b36c18e
        ('j193HsnW72Yqns7u', 'j193hsne720uie8i.cc', ('com', 'net', 'biz', 'org'), 100),
    ]


    # Hard-coded c2 domains:
    # (see https://www.symantec.com/security_response/writeup.jsp?docid=2014-092411-3132-99&tabid=2)
    hard_coded = []
    hard_coded.extend(
        ('newstatinru.ru', 'justforyou0987.pw', 'phpsitegooddecoder.com'))


    # The page below mentions DNS requests to several domains that this DGA
    # does not generate.  Perhaps they are hard-coded in some samples.
    # https://www.sophos.com/en-us/threat-center/threat-analyses/viruses-and-spyware/Troj~Wonton-MT/detailed-analysis.aspx
    hard_coded.extend(
        ('santaluable.com', 'santanyr.com', 'ervaluable.com', 'larnasa.com'))


    for domain in hard_coded:
        print(domain)

    for config in dga_configurations:
        for result in dga(*config):
            print(result)
