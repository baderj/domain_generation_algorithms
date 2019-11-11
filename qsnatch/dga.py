import time
import hashlib
import base64
import argparse
from datetime import datetime


TLDS = {
    "cf": 0, "tk": 0, "com": 1, "ml": 0, "de": 0, "rocks": 0, "mx": 0,
    "biz": 0, "net": 1, "cn": 0, "ga": 0, "gq": 0, "org": 1, "top": 0, "nl": 0,
    "men": 0, "ws": 0, "se": 0, "info": 0, "xyz": 0, "today": 0, "ru": 0,
    "ec": 0, "co": 0, "ee": 0, "rs": 0, "com.sv": 0, "com.cy": 0, "co.zw": 0,
    "kg": 0, "com.ge": 0, "tl": 0, "name": 0, "tw": 0, "lv": 0, "bs": 0,
    "li": 0, "ng": 0, "ae": 0, "bt": 0, "tv": 0, "pe": 0, "uz": 0, "me": 0,
    "gy": 0, "am": 0, "kr": 0, "by": 0, "fr": 0, "com.uy": 0, "com.lb": 0,
    "com.br": 0, "vu": 0, "hk": 0, "in": 0, "re": 0, "ch": 0, "af": 0,
    "com.ps": 0, "ug": 0, "dz": 0, "pro": 0, "co.th": 0, "sg": 0, "cd": 0,
    "so": 0, "mo": 0, "co.id": 0, "co.il": 0, "com.do": 0, "ke": 0, "cx": 0,
    "ro": 0, "id": 0, "pm": 0, "hm": 0, "vg": 0, "az": 0, "com.eg": 0, "bz": 0,
    "su": 0, "com.ar": 0, "gg": 0, "com.lr": 0, "pa": 0, "com.ve": 0, "al": 0,
    "fm": 0, "to": 0, "mu": 0, "co.ck": 0, "pk": 0, "co.rs": 0, "cw": 0,
    "nr": 0, "gd": 0, "gl": 0, "ac": 0, "lk": 0, "md": 0, "fi": 0, "sx": 0,
    "lc": 0, "es": 0, "cc": 0, "cm": 0, "la": 0, "co.za": 0, "je": 0, "cz": 0,
    "jp": 0, "ai": 0, "pw": 0, "bg": 0, "nu": 0, "ag": 0, "bm": 0, "eu": 0,
    "com.my": 0, "sc": 0, "ax": 0, "wf": 0, "ly": 0, "qa": 0, "vn": 0, "aq": 0,
    "mobi": 0, "com.tr": 0, "com.ua": 0, "com.py": 0, "hk.org": 0,
    "south.am": 0, "com.kh": 0, "co.zm": 0, "ru.net": 0, "com.km": 0, "tt": 0,
    "kn": 0, "co.ls": 0, "co.fk": 0, "uy.com": 0, "com.gu": 0, ".com.bn": 0,
    "com.pf": 0, "com.fj": 0
}
SEED = "IbjGOEgnuD"


def dga(date):
    def unix(date):
        unix = int(time.mktime(date.timetuple()))
        return unix

    HOUR = 3600
    DAY = 24*HOUR
    for interval in [15*DAY, 5*DAY, 1*DAY, 8*HOUR, 2*HOUR, 1*HOUR]:
        for length in [5, 3, 4]:
            for tld, l in TLDS.items():
                min_length = l + length
                key = f"{unix(date)//interval}{SEED}{tld}\n".encode('ascii')
                key_hash = hashlib.sha1(key).digest()
                key_hash_b64 = base64.b64encode(key_hash).decode('ascii')
                key_hash_b64_noeq_lc = key_hash_b64.rstrip("=").lower()
                trantab = str.maketrans("-+/", "abc")
                sld_src = key_hash_b64_noeq_lc.translate(trantab)
                sld_len = max(min_length, 3)
                sld = sld_src[:sld_len]
                domain = f"{sld}.{tld}"
                yield domain


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QSnatch dga")
    parser.add_argument(
        "-d", "--datetime",
        help="date time for which to generate domains, e.g., "
             "2019-11-11 18:00:00")
    args = parser.parse_args()
    if args.datetime:
        d = datetime.strptime(args.datetime, "%Y-%m-%d %H:%M:%S")
    else:
        d = datetime.now()
    for domain in dga(d):
        print(domain)
