from datetime import datetime
import struct
import argparse


class RC4:

    def __init__(self, key_s):
        key = [ord(k) for k in key_s]

        S = 256*[0]
        for i in range(256):
            S[i] = i

        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]

        self.S = S
        self.i = 0
        self.j = 0

    def prng(self):
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.S[self.i]) % 256
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
        K = self.S[(self.S[self.i] + self.S[self.j]) % 256]
        return K

    def encrypt(self, data):
        res = bytearray()
        for d in data:
            c = d ^ self.prng()
            res.append(c)
        return res

    def __str__(self):
        r = ""
        for i, s in enumerate(self.S):
            r += f"{i}: {hex(s)}\n"
        return r


def seeding(d, key):
    rc4 = RC4(key)
    d = d.replace(hour=0, minute=0, second=0)
    timestamp = int((d - datetime(1970, 1, 1)).total_seconds())
    p = struct.pack("<I", timestamp)
    c = rc4.encrypt(p)
    seed = struct.unpack("<I", c)[0]
    return seed


def dga(seed, nr_of_domains):
    r = seed
    for i in range(nr_of_domains):
        domain = ""
        for j in range(20):
            letter = ord('a') + (r % 25)
            domain += chr(letter)
            r = seed ^ ((r + letter) & 0xFFFFFFFF)
        domain += ".com"
        print(domain)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date when domains are generated")
    parser.add_argument("-r", "--rc4", 
            help="rc4 key from config",
            choices=["q23Cud3xsNf3","41997b4a729e1a0175208305170752dd", "kZieCw23gffpe43Sd",  "Ts72YjsjO5TghE6m", "03d5ae30a0bd934a23b6a7f0756aa504"],
            default="q23Cud3xsNf3")


    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    seed = seeding(d, args.rc4)
    dga(seed, 32)
