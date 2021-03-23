def dga(seed, nr):
    s = (2 * seed * (nr + 1))
    r = s ^ (26 * seed * nr)
    domain = ""
    for i in range(16):
        r = r & 0xFFFFFFFF
        domain += chr(r % 26 + ord('a'))
        r += (r ^ (s*i**2*26))
 
    domain += ".org"
    return domain

for nr in range(20):
    print(dga(0xD5FFF, nr))


