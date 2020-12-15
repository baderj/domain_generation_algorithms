from itertools import product
from datetime import datetime
import argparse
from collections import namedtuple

Param = namedtuple('Param', 'mul mod idx')
pool = (
    "qeewcaacywemomedekwyuhidontoibeludsocuexvuuftyliaqydhuizuctuiqow"
    "agypetehfubitiaziceblaogolryykosuptaymodisahfiybyxcoleafkudarapu"
    "qoawyluxqagenanyoxcygyqugiutlyvegahepovyigqyqibaeqynyfkiobpeepby"
    "xaciyvusocaripfyoftesaysozureginalifkazaadytwuubzuvoothymivazyyz"
    "hoevmeburedeviihiravygkemywaerdonoyryqloammoseweesuvfopiriboikuz"
    "orruzemuulimyhceukoqiwfexuefgoycwiokitnuneroxepyanbekyixxiuqsias"
    "xoapaxmaohezwoildifaluzihipanizoecxyopguakdudyovhaumunuwsusyenko"
    "atugabiv"
)


def dga(date):
    seed = date.strftime("%m%Y")
    params = [
        Param(19, 19, 0),
        Param(19, 19, 1),
        Param(6, 6, 4),
        Param(6, 6, 5)
    ]
    ranges = []
    for p in params:
        s = int(seed[p.idx])
        lower = p.mul*s
        upper = lower + p.mod
        ranges.append(list(range(lower, upper)))

    for indices in product(*ranges):
        domain = ""
        for index in indices:
            domain += pool[index*2:index*2 + 2]
        domain += ".bazar"
        yield domain


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--date", help="date used for seeding, e.g., 2020-06-28",
        default=datetime.now().strftime('%Y-%m-%d'))
    args = parser.parse_args()
    d = datetime.strptime(args.date, "%Y-%m-%d")
    for domain in dga(d):
        print(domain)
