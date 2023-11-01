"""
    seed 0x56EDC15 from my own analysis of 
    md5: 2838cd03b6c0a414c8edb4d4a333ff94

    seed 0x5397FB1 reversed engineered from sample in
    https://blog.netlab.360.com/an-analysis-of-linux-ngioweb-botnet-en/

    seeds 0x01275c63, 0x04bc65bc and 0x00375d5a taken from 
    https://blog.netlab.360.com/linux-ngioweb-v2-going-after-iot-devices-en/
"""
from dataclasses import dataclass
import argparse


@dataclass
class Blocks:
    vowels = "aeiou"
    consonants = "bcdfghklmnprstvxz"
    prefix_words = ["un", "under", "re", "in", "im", "il", "ir", "en", "em", "over",
        "mis", "dis", "pre", "post", "anti", "inter", "sub", "ultra", "non", "de",
        "pro", "trans", "ex", "macro", "micro", "mini", "mono", "multi", "semi", "co"]
    vowel_words = ["able", "ant", "ate", "age", "ance", "ancy", "an", "ary", "al",
        "en", "ency", "er", "etn", "ed", "ese", "ern", "ize", "ify", "ing", "ish",
        "ity", "ion", "ian", "ism", "ist", "ic", "ical", "ible", "ive", "ite", "ish",
        "ian", "or", "ous", "ure"]
    consonant_words = ["dom", "hood", "less", "like", "ly", "fy", "ful", "ness",
        "ment", "sion", "ssion", "ship", "ty", "th", "tion", "ward"]
    tlds = [".net", ".info", ".com", ".biz", ".org", ".name"]


class Rand:
    def __init__(self, seed):
        self.seed = seed
        self.r = self.seed

    def rand(self, mod: int):
        self.r = (1103515245 * self.r + 12345) & 0xFFFFFFFF
        return self.r % mod

    def random_el_from_list(self, l: [str]) -> str:
        return l[self.rand(len(l))]


def ends_in_consonant(domain: str) -> bool:
    return domain[-1] not in Blocks.vowels


def dga(r):
    domain = ""
    nr_parts = r.rand(3) + 1
    for i in range(nr_parts):
        domain += r.random_el_from_list(Blocks.prefix_words)
        pick_vowel = ends_in_consonant(domain)
        for _ in range(r.rand(3) + 4):
            l = Blocks.vowels if pick_vowel else Blocks.consonants
            domain += r.random_el_from_list(l)
            pick_vowel ^= 1

        l = Blocks.vowel_words if ends_in_consonant(domain) else Blocks.consonant_words
        domain += r.random_el_from_list(l)
        domain += "-" if i < nr_parts - 1 else ""

    return domain + r.random_el_from_list(Blocks.tlds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--seed",
        help="Seed for the random generator (hex)",
        choices=["5397FB1", "56EDC15", "01275c63", "04bc65bc", "00375d5a"],
        default="56EDC15",
    )
    parser.add_argument("-n", "--nr", help="nr of domains", default=0x400, type=int)
    args = parser.parse_args()
    args.seed = int(args.seed, 16)
    r = Rand(args.seed)
    for i in range(args.nr):
        domain = dga(r)
        print(domain)
