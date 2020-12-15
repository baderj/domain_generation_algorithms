import json
import argparse
from datetime import datetime
import time
import struct
from md6 import md6hash


def hash(nr):
    data = struct.pack("<I", nr)
    return md6hash().hex(data)

def seeding(nr):

    MASK = 0xFFFFFFFF

    def lcg_random(values, index, result):
        LCG_MULT = 22695477
        v = values[index]
        v *= LCG_MULT
        v &= MASK 
        v += 1
        v &= MASK 
        values[index] = v

        a = (v >> 16)
        a &= 0x7FFF
        shift = result & 0xF
        a += result
        a &= MASK
        result = lrotl(a, shift)
        return result


    def lcg_random_rounds(values, result=0):
        for index in range(size):
            for r in range(index+1):
                result = lcg_random(values, index, result)
        return result

    def xor_encryption(values, key, result):
        for index in range(len(values)):
            result = lcg_random(values, index, result)
        nkey = key ^ (result & 0xFF)
        result += key
        result &= MASK
        values[-1] = ((values[-1] + key) & MASK)
        return nkey, result

    def lrotl(value, shift):
        overflow = ((value << shift) >> 32) & MASK
        value = (value << shift)
        value += overflow 
        value &= MASK
        return value

    def transform(seed_padded, values, result, rounds, offset=0):
        index = offset
        while rounds:
            if index >= len(seed_padded):
                index = 0
            key = seed_padded[index]
            nkey, result = xor_encryption(values, key, result)
            nkey ^= key
            seed_padded[index] = nkey
            index += 1
            rounds -= 1
        return result

    seed = hash(nr)
    tuples = [seed[i:i+2] for i in range(0, len(seed), 2)]

    values = []
    for t in tuples:
        v = ord(t[0])*256 + ord(t[1])
        values.append(v)

    size = 0x80
    while len(values) < size:
        values.append(0)

    result = lcg_random_rounds(values)


    seed_padded = bytearray()
    for i in range(0x100): 
        if i < len(seed):
            seed_padded.append(ord(seed[i]))
        else:
            seed_padded.append(0)

    numerator = len(seed_padded) 
    result = transform(seed_padded, values, result, rounds=numerator)
    numerator = (numerator+1)*10
    result = transform(seed_padded, values, result, rounds=numerator, offset=len(seed_padded)-1) 

    values = []
    for i in range(0, len(seed_padded), 2):
        values.append(seed_padded[i]*256 + seed_padded[i+1])

    result = lcg_random_rounds(values)
    offset = nr % 50
    key_string = seed[offset:offset+4] 

    seed = 0 
    for i, key in enumerate(key_string):
        key = ord(key)
        nkey, result = xor_encryption(values, key, result)
        seed += (nkey << (i*8))

    return seed


def get_sld(length, seed):
    sld = ""
    modulo = 541 * length + 4
    a = length * length
    for i in range(length):
        index = (a + (seed*((seed % 5) + (seed % 123456) +
                            i*((seed & 1) + (seed % 4567))) & 0xFFFFFFFF)) % 26
        a += length
        a &= 0xFFFFFFFFF
        sld += chr(ord('a') + index)
        seed += (((7837632 * seed * length) & 0xFFFFFFFF) + 82344) % modulo
    return sld


def generate_domains(date, nr, set_nr):
    dt = time.mktime(date.timetuple())
    days = 20 if set_nr == 1 else 1
    index = int(dt//(days*3600*24))

    seed = seeding(index)

    for dga_nr in range(nr):
        # determine next seed
        s = seed % (dga_nr + 1)
        seed += (s + 1)

        # second level length
        length = (seed + dga_nr) % 7 + 6

        # get second level domain
        second_level_domain = get_sld(length, seed)

        # get first level domain
        tlds = ['com', 'net', 'org', 'info', 'cc']
        top_level_domain = tlds[(seed & 3)]

        # concatenate and print domain
        domain = second_level_domain + '.' + top_level_domain
        print(domain)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--date", help="date for which to generate domains")
    parser.add_argument(
        "-n", "--nr", help="nr of domains to generate", type=int, default=10)
    parser.add_argument("-s", "--set_nr", help="seeds set, 1 = useful dga, 2 = noise dga",
                        type=int, default=1, choices=[1, 2])
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.utcnow()
    generate_domains(d, args.nr, args.set_nr)
