import argparse
from collections import namedtuple
from datetime import datetime
from itertools import product

Param = namedtuple("Param", "mul mod idx")

p1 = (
    "qeewcaacywemomedekwyuhidontoibeludsocuexvuuftyliaqydhuizuctuiqow"
    "agypetehfubitiaziceblaogolryykosuptaymodisahfiybyxcoleafkudarapu"
    "qoawyluxqagenanyoxcygyqugiutlyvegahepovyigqyqibaeqynyfkiobpeepby"
    "xaciyvusocaripfyoftesaysozureginalifkazaadytwuubzuvoothymivazyyz"
    "hoevmeburedeviihiravygkemywaerdonoyryqloammoseweesuvfopiriboikuz"
    "orruzemuulimyhceukoqiwfexuefgoycwiokitnuneroxepyanbekyixxiuqsias"
    "xoapaxmaohezwoildifaluzihipanizoecxyopguakdudyovhaumunuwsusyenko"
    "atugabiv"
)

p2 = (
    "yzewevmeywreomviekwyavygontowaerudsoyrexvuamtyseweesuvizpituiqow"
    "uzoretzemuultiazicukoqiwolxuykosupwiymitisneroxeyxanlekyixxirasi"
    "asxoapuxqaohezwooxdigyquziutpavezohexyvyguqyqidyovynumunuwsusyen"
    "xaatyvusivaripfyoftesaysozureginalif"
)

p3 = (
    "xezeiwzuizpizovureonxyuzofezytpuarywnyavrysiovvazyratuoskumuatyz"
    "omnevexaqoixevkeuqoxuvutvipoymxoozwikonipysygotelyzayxnuunuwakqu"
    "ritaamugvyitimsuyrwyxuexaqtigyivewqiydseawukhirufuwairkiiquxowih"
    "hyurotiluhvocywowumoyvupagduobaserroziqyenpahaxiloazodtoishuax"
)

p4 = (
    "xezenozuizpioqvuekifxyusofalytkadeibubysmyliylvaikultugikuuddoyq"
    "lanevebaqoixogicuqebuvbuviehbofyefsokonihosygoynbeetwenuunuwohqu"
    "ritaamugvyitimfiyrelcoykaqqaacapokcuydseumafedemfubyirahiquxegce"
    "aburotiluhvocywowumoyvupagduobaserroziqyenpahaxiloazodtoishuaxbi"
    "ufmifoiwesleyhzoyfreontyuzfaezkypuarywnyavrysiovyczyraciosgumuat"
    "yzommeolxaeqdaevkepeoxsauteppoymxoozwiygucpyheectelyzayxybgaypak"
    "igluinmacageocidsuorwyxuexantigyivewqiadnaawukhirudywaqekidiipow"
    "ihhyopfexezenozuizpioqvuekifxyusofalytkadeibubysmyliylvaikultugi"
    "kuuddoyqlanevebaqoixogicuqebuvbuviehbofyefsokonihosygoynbeetwenu"
    "unuwohquritaamugvyitimfiyrelcoykaqqaacapokcuydseumafedemfubyirah"
    "iquxegceaburotiluhvocywowumoyvupagduobaserroziqyenpahaxiloazodto"
    "ishuaxbiufmifoiwesleyhzoyfreontyuzfaezkypuarywnyavrysiovyczyraci"
    "osgumuatyzommeolxaeqdaevkepeoxsauteppoymxoozwiygucpyheectelyzayx"
    "ybgaypakigluinmacageocidsuorwyxuexantigyivewqiadnaawukhirudywaqe"
    "kidiipowihhyopfe"
)


c1 = [Param(19, 19, 0), Param(19, 19, 1), Param(6, 6, 4), Param(6, 6, 5)]
c2 = [Param(19, 19, 0), Param(19, 19, 1), Param(4, 22, 4), Param(4, 4, 5)]
c3 = [Param(19, 19, 0), Param(19, 19, 1), Param(4, 4, 4), Param(4, 4, 5)]

versions = {
    "v2": (p1, c1),
    "v3": (p1, c2),
    "v4": (p2, c2),
    "v5": (p1, c3),
    "v6": (p3, c3),
    "v7": (p4, c3),
}


def dga(date: datetime, version: str):
    seed = date.strftime("%m%Y")
    print(seed)
    pool, params = versions[version]
    ranges = []
    for p in params:
        s = int(seed[p.idx])
        lower = p.mul * s
        upper = lower + p.mod
        ranges.append(list(range(lower, upper)))

    for indices in product(*ranges):
        domain = ""
        for index in indices:
            domain += pool[index * 2 : index * 2 + 2]
        domain += ".bazar"
        yield domain


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--date",
        help="date used for seeding, e.g., 2020-06-28",
        default=datetime.now().strftime("%Y-%m-%d"),
    )
    parser.add_argument(
        "-v",
        "--version",
        help="version",
        choices=versions.keys(),
        default="v2",
    )
    args = parser.parse_args()
    d = datetime.strptime(args.date, "%Y-%m-%d")
    for domain in dga(d, args.version):
        print(domain)
