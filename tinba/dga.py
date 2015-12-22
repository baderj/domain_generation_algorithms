seed ="j193HsnW72Yqns7u"
seed += (17 - len(seed))*"\x00"
seed_l = [ord(s) for s in seed]
domain = "j193hsne720uie8i.cc"
print(domain)
for i in range(100):
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
                
    for tld in ['com', 'net', 'biz', 'org']:
        domain = ''.join([chr(x) for x in new_domain]) + '.' + tld
        print(domain)
